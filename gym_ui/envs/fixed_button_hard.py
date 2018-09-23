import numpy as np

from gym_ui.envs import FixedButton


class FixedButtonHard(FixedButton):

    def __init__(self):
        super().__init__()
        self.button_positions = np.random.rand(10, 2) * 0.75 + 0.125
        self.button_size = 0.25
