import random
import time
import gym
import numpy as np
from gym import spaces


class FixedButton(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    padding_value = -1

    def __init__(self):
        random.seed(1)
        self.button_positions = np.random.rand(3, 2) * 0.5 + 0.25

        self.screen_res = 50

        # A list of player ratings
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.screen_res, self.screen_res, 3), dtype=np.uint8)
        # Indexes for the two players we want to match
        self.action_space = spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32)
        self.viewer = None
        self.button_position_idx = 0
        self.click_position = None
        self.button_transform = None
        self.click_transform = None

        self.button_size = 0.5
        self.click_size = 0.1

    def seed(self, seed=None):
        random.seed(seed)

    def step(self, action):
        action = np.clip(action, 0, 1)
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        self.click_position = action
        distance = self.distance_to_button_border()
        button_pos = self.button_positions[self.button_position_idx]

        if distance == 0:
            reward = 1 if self.button_position_idx == len(self.button_positions) - 1 else 0
            self.change_button_position()
        else:
            reward = 0

        start_time = time.time()
        frame = self.render(mode='rgb_array')
        # print("Rendering :", time.time() - start_time)

        return frame, reward, False, {'distance_border': distance, 'button_x': button_pos[0], 'button_y': button_pos[1]}

    def reset(self):
        self.change_button_position()
        self.click_position = (0, 0)
        return self.render(mode='rgb_array')

    def change_button_position(self):
        self.button_position_idx = (self.button_position_idx + 1) % np.shape(self.button_positions)[0]

    def render(self, mode='human'):

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(self.screen_res, self.screen_res)

            self.button_transform, button_color = self.create_polygon(rendering, self.button_size * self.screen_res)
            button_color.vec4 = (0, 0, 0, 1)

            self.click_transform, click_color = self.create_polygon(rendering, self.click_size * self.screen_res)
            click_color.vec4 = (1, 0, 0, 1)

        button_pos = self.button_positions[self.button_position_idx]
        self.button_transform.set_translation(self.screen_res * button_pos[0], self.screen_res * button_pos[1])
        self.click_transform.set_translation(self.screen_res * self.click_position[0], self.screen_res * self.click_position[1])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def create_polygon(self, rendering, size):
        l, r, t, b = -size / 2, size / 2, size / 2, -size / 2
        polygon = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
        transform = rendering.Transform()
        polygon.add_attr(transform)
        color = polygon.attrs[0]

        self.viewer.add_geom(polygon)

        return transform, color

    def distance_to_button_border(self):
        button_position_scaled = self.button_positions[self.button_position_idx]

        click_position_scaled = self.click_position

        dx = max(abs(click_position_scaled[0] - button_position_scaled[0]) - self.button_size / 2, 0)
        dy = max(abs(click_position_scaled[1] - button_position_scaled[1]) - self.button_size / 2, 0)

        return dx * dx + dy * dy
