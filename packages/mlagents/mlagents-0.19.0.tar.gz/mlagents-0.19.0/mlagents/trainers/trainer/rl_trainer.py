# # Unity ML-Agents Toolkit
import os
from typing import Dict, List, Optional
from collections import defaultdict
import abc
import time
import attr
from mlagents.model_serialization import SerializationSettings, copy_model_files
from mlagents.trainers.policy.checkpoint_manager import (
    NNCheckpoint,
    NNCheckpointManager,
)
from mlagents_envs.logging_util import get_logger
from mlagents_envs.timers import timed
from mlagents.trainers.optimizer import Optimizer
from mlagents.trainers.buffer import AgentBuffer
from mlagents.trainers.trainer import Trainer
from mlagents.trainers.components.reward_signals import RewardSignalResult
from mlagents_envs.timers import hierarchical_timer
from mlagents.trainers.agent_processor import AgentManagerQueue
from mlagents.trainers.trajectory import Trajectory
from mlagents.trainers.stats import StatsPropertyType

RewardSignalResults = Dict[str, RewardSignalResult]

logger = get_logger(__name__)


class RLTrainer(Trainer):  # pylint: disable=abstract-method
    """
    This class is the base class for trainers that use Reward Signals.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # collected_rewards is a dictionary from name of reward signal to a dictionary of agent_id to cumulative reward
        # used for reporting only. We always want to report the environment reward to Tensorboard, regardless
        # of what reward signals are actually present.
        self.cumulative_returns_since_policy_update: List[float] = []
        self.collected_rewards: Dict[str, Dict[str, int]] = {
            "environment": defaultdict(lambda: 0)
        }
        self.update_buffer: AgentBuffer = AgentBuffer()
        self._stats_reporter.add_property(
            StatsPropertyType.HYPERPARAMETERS, self.trainer_settings.as_dict()
        )
        self._next_save_step = 0
        self._next_summary_step = 0

    def end_episode(self) -> None:
        """
        A signal that the Episode has ended. The buffer must be reset.
        Get only called when the academy resets.
        """
        for rewards in self.collected_rewards.values():
            for agent_id in rewards:
                rewards[agent_id] = 0

    def _update_end_episode_stats(self, agent_id: str, optimizer: Optimizer) -> None:
        for name, rewards in self.collected_rewards.items():
            if name == "environment":
                self.stats_reporter.add_stat(
                    "Environment/Cumulative Reward", rewards.get(agent_id, 0)
                )
                self.cumulative_returns_since_policy_update.append(
                    rewards.get(agent_id, 0)
                )
                self.reward_buffer.appendleft(rewards.get(agent_id, 0))
                rewards[agent_id] = 0
            else:
                self.stats_reporter.add_stat(
                    optimizer.reward_signals[name].stat_name, rewards.get(agent_id, 0)
                )
                rewards[agent_id] = 0

    def _clear_update_buffer(self) -> None:
        """
        Clear the buffers that have been built up during inference.
        """
        self.update_buffer.reset_agent()

    @abc.abstractmethod
    def _is_ready_update(self):
        """
        Returns whether or not the trainer has enough elements to run update model
        :return: A boolean corresponding to wether or not update_model() can be run
        """
        return False

    def _policy_mean_reward(self) -> Optional[float]:
        """ Returns the mean episode reward for the current policy. """
        rewards = self.cumulative_returns_since_policy_update
        if len(rewards) == 0:
            return None
        else:
            return sum(rewards) / len(rewards)

    @timed
    def _checkpoint(self) -> NNCheckpoint:
        """
        Checkpoints the policy associated with this trainer.
        """
        n_policies = len(self.policies.keys())
        if n_policies > 1:
            logger.warning(
                "Trainer has multiple policies, but default behavior only saves the first."
            )
        policy = list(self.policies.values())[0]
        model_path = policy.model_path
        settings = SerializationSettings(model_path, self.brain_name)
        checkpoint_path = os.path.join(model_path, f"{self.brain_name}-{self.step}")
        policy.checkpoint(checkpoint_path, settings)
        new_checkpoint = NNCheckpoint(
            int(self.step),
            f"{checkpoint_path}.nn",
            self._policy_mean_reward(),
            time.time(),
        )
        NNCheckpointManager.add_checkpoint(
            self.brain_name, new_checkpoint, self.trainer_settings.keep_checkpoints
        )
        return new_checkpoint

    def save_model(self) -> None:
        """
        Saves the policy associated with this trainer.
        """
        n_policies = len(self.policies.keys())
        if n_policies > 1:
            logger.warning(
                "Trainer has multiple policies, but default behavior only saves the first."
            )
        policy = list(self.policies.values())[0]
        model_checkpoint = self._checkpoint()

        # Copy the checkpointed model files to the final output location
        copy_model_files(model_checkpoint.file_path, f"{policy.model_path}.nn")

        final_checkpoint = attr.evolve(
            model_checkpoint, file_path=f"{policy.model_path}.nn"
        )
        NNCheckpointManager.track_final_checkpoint(self.brain_name, final_checkpoint)

    @abc.abstractmethod
    def _update_policy(self) -> bool:
        """
        Uses demonstration_buffer to update model.
        :return: Whether or not the policy was updated.
        """
        pass

    def _increment_step(self, n_steps: int, name_behavior_id: str) -> None:
        """
        Increment the step count of the trainer
        :param n_steps: number of steps to increment the step count by
        """
        self.step += n_steps
        self._next_summary_step = self._get_next_interval_step(self.summary_freq)
        self._next_save_step = self._get_next_interval_step(
            self.trainer_settings.checkpoint_interval
        )
        p = self.get_policy(name_behavior_id)
        if p:
            p.increment_step(n_steps)

    def _get_next_interval_step(self, interval: int) -> int:
        """
        Get the next step count that should result in an action.
        :param interval: The interval between actions.
        """
        return self.step + (interval - self.step % interval)

    def _write_summary(self, step: int) -> None:
        """
        Saves training statistics to Tensorboard.
        """
        self.stats_reporter.add_stat("Is Training", float(self.should_still_train))
        self.stats_reporter.write_stats(int(step))

    @abc.abstractmethod
    def _process_trajectory(self, trajectory: Trajectory) -> None:
        """
        Takes a trajectory and processes it, putting it into the update buffer.
        :param trajectory: The Trajectory tuple containing the steps to be processed.
        """
        self._maybe_write_summary(self.get_step + len(trajectory.steps))
        self._maybe_save_model(self.get_step + len(trajectory.steps))
        self._increment_step(len(trajectory.steps), trajectory.behavior_id)

    def _maybe_write_summary(self, step_after_process: int) -> None:
        """
        If processing the trajectory will make the step exceed the next summary write,
        write the summary. This logic ensures summaries are written on the update step and not in between.
        :param step_after_process: the step count after processing the next trajectory.
        """
        if self._next_summary_step == 0:  # Don't write out the first one
            self._next_summary_step = self._get_next_interval_step(self.summary_freq)
        if step_after_process >= self._next_summary_step and self.get_step != 0:
            self._write_summary(self._next_summary_step)

    def _maybe_save_model(self, step_after_process: int) -> None:
        """
        If processing the trajectory will make the step exceed the next model write,
        save the model. This logic ensures models are written on the update step and not in between.
        :param step_after_process: the step count after processing the next trajectory.
        """
        if self._next_save_step == 0:  # Don't save the first one
            self._next_save_step = self._get_next_interval_step(
                self.trainer_settings.checkpoint_interval
            )
        if step_after_process >= self._next_save_step and self.get_step != 0:
            self._checkpoint()

    def advance(self) -> None:
        """
        Steps the trainer, taking in trajectories and updates if ready.
        Will block and wait briefly if there are no trajectories.
        """
        with hierarchical_timer("process_trajectory"):
            for traj_queue in self.trajectory_queues:
                # We grab at most the maximum length of the queue.
                # This ensures that even if the queue is being filled faster than it is
                # being emptied, the trajectories in the queue are on-policy.
                _queried = False
                for _ in range(traj_queue.qsize()):
                    _queried = True
                    try:
                        t = traj_queue.get_nowait()
                        self._process_trajectory(t)
                    except AgentManagerQueue.Empty:
                        break
                if self.threaded and not _queried:
                    # Yield thread to avoid busy-waiting
                    time.sleep(0.0001)
        if self.should_still_train:
            if self._is_ready_update():
                with hierarchical_timer("_update_policy"):
                    if self._update_policy():
                        for q in self.policy_queues:
                            # Get policies that correspond to the policy queue in question
                            q.put(self.get_policy(q.behavior_id))
        else:
            self._clear_update_buffer()
