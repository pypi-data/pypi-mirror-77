import argparse
from unittest import TestCase
import numpy as np
import gym
import torch

from pl_bolts.datamodules.experience_source import DiscountedExperienceSource
from pl_bolts.models.rl.common import cli
from pl_bolts.models.rl.common.agents import Agent
from pl_bolts.models.rl.common.networks import MLP
from pl_bolts.models.rl.common.wrappers import ToTensor
from pl_bolts.models.rl.dqn_model import DQN
from pl_bolts.models.rl.reinforce_model import Reinforce


class TestReinforce(TestCase):

    def setUp(self) -> None:
        self.env = ToTensor(gym.make("CartPole-v0"))
        self.obs_shape = self.env.observation_space.shape
        self.n_actions = self.env.action_space.n
        self.net = MLP(self.obs_shape, self.n_actions)
        self.agent = Agent(self.net)
        self.exp_source = DiscountedExperienceSource(self.env, self.agent)

        parent_parser = argparse.ArgumentParser(add_help=False)
        parent_parser = cli.add_base_args(parent=parent_parser)
        parent_parser = DQN.add_model_specific_args(parent_parser)
        args_list = [
            "--algo", "dqn",
            "--warm_start_steps", "500",
            "--episode_length", "100",
            "--env", "CartPole-v0",
            "--batch_size", "32",
            "--gamma", "0.99"
        ]
        self.hparams = parent_parser.parse_args(args_list)
        self.model = Reinforce(**vars(self.hparams))

        self.rl_dataloader = self.model.train_dataloader()

    def test_loss(self):
        """Test the reinforce loss function"""

        batch_states = torch.rand(32, 4)
        batch_actions = torch.rand(32).long()
        batch_qvals = torch.rand(32)

        loss = self.model.loss(batch_states, batch_actions, batch_qvals)

        self.assertIsInstance(loss, torch.Tensor)

    def test_get_qvals(self):
        """Test that given an batch of episodes that it will return a list of qvals for each episode"""

        batch_qvals = []
        rewards = np.ones(32)
        out = self.model.calc_qvals(rewards)
        batch_qvals.append(out)

        self.assertIsInstance(batch_qvals[0][0], float)
        self.assertEqual(batch_qvals[0][0], (batch_qvals[0][1] * self.hparams.gamma) + 1.0)

    def test_calc_q_vals(self):
        rewards = np.ones(4)
        gt_qvals = [3.9403989999999998, 2.9701, 1.99, 1.0]

        qvals = self.model.calc_qvals(rewards)

        self.assertEqual(gt_qvals, qvals)
