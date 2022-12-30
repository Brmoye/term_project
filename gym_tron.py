import gym
import os
from gym.spaces import Discrete, Box, MultiDiscrete
import numpy as np
from Game import Game
from tron import *
import pygame as py
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv
from gym.envs.registration import register
import random
import copy

class TronEnv(gym.Env):
    metadata = {"render.modes": ["human"]}
    def __init__(self, cycles, board_size=400, scale=2):
        super(TronEnv, self).__init__()
        self.board_size = board_size
        self.scale = scale
        self.cycles = cycles
        self.board = Board(self.board_size, copy.deepcopy(self.cycles), self.scale)

        self.action_space = Discrete(4)
        self.observation_space = Box(low=0, high=10, shape=(np.array([self.board_size*self.board_size,])),dtype=np.float32)
        # self.observation_space = MultiDiscrete([10 for _ in range(self.board_size*self.board_size)])
        
    def step(self, action):
        self.board.turn(action + 1)
        obs = self.board.observe()
        reward = self.board.evaluate()
        done = self.board.game_status()
        return obs, reward, done, {}
        
    def render(self, mode='bot', close=False):
        self.board.view()
    
    def reset(self):
        del self.board
        self.board = Board(self.board_size, copy.deepcopy(self.cycles), self.scale)
        obs = self.board.observe()
        return obs
        

register(
    # unique identifier for the env `name-version`
    id="TronEnv-v1",
    # path to the class for creating the env
    # Note: entry_point also accept a class as input (and not only a string)
    entry_point=".\gym_tron",
    # Max number of steps per episode, using a `TimeLimitWrapper`
    max_episode_steps=500,
)

