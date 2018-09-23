import random
import time
import gym
import numpy as np
from gym import spaces

from gym_ui.envs import FixedButton


class RandomButton(FixedButton):

    def __init__(self):
        super().__init__()
        self.button_position_idx = 0

    def change_button_position(self):
        self.button_positions = np.random.rand(1, 2) * 0.5 + 0.25
