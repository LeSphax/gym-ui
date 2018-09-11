import random
import time
import gym
import numpy as np
from gym import spaces


class RandomButton(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    padding_value = -1

    def __init__(self):
        self.screen_size = 50

        # A list of player ratings
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.screen_size, self.screen_size, 3), dtype=np.uint8)
        # Indexes for the two players we want to match
        self.action_space = spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32)
        self.viewer = None
        self.button_position = None
        self.click_position = None
        self.button_transform = None
        self.click_transform = None

        self.button_size = 25.0
        self.click_size = 5.0

    def seed(self, seed=None):
        random.seed(seed)

    def step(self, action):
        action= np.clip(action, 0, 1)
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        self.click_position = action

        if self.is_click_on_button():
            reward = 1
            self.change_button_position()
        else:
            reward = 0

        start_time = time.time()
        frame = self.render(mode='rgb_array')
        # print("Rendering :", time.time() - start_time)

        return frame, reward, False, {}

    def reset(self):
        self.change_button_position()
        self.click_position = (0, 0)
        return self.render(mode='rgb_array')

    def change_button_position(self):
        self.button_position = np.array([random.random()*0.5 + 0.25, random.random()*0.5 + 0.25])

    def render(self, mode='human'):

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(self.screen_size, self.screen_size)

            self.button_transform, button_color = self.create_polygon(rendering, self.button_size)
            button_color.vec4 = (0, 0, 0, 1)

            self.click_transform, click_color = self.create_polygon(rendering, self.click_size)
            click_color.vec4 = (1, 0, 0, 1)

        self.button_transform.set_translation(self.screen_size * self.button_position[0], self.screen_size * self.button_position[1])
        self.click_transform.set_translation(self.screen_size * self.click_position[0], self.screen_size * self.click_position[1])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def create_polygon(self, rendering, size):
        l, r, t, b = -size / 2, size / 2, size / 2, -size / 2
        polygon = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
        transform = rendering.Transform()
        polygon.add_attr(transform)
        color = polygon.attrs[0]

        self.viewer.add_geom(polygon)

        return transform, color

    def is_click_on_button(self):
        l, r, t, b = -self.button_size / 2, self.button_size / 2, self.button_size / 2, -self.button_size / 2

        button_position_scaled = self.button_position * self.screen_size

        l, r = map(lambda x: x + button_position_scaled[0], [l, r])
        t, b = map(lambda x: x + button_position_scaled[1], [t, b])

        click_position_scaled = self.click_position * self.screen_size

        if l < click_position_scaled[0] < r:
            if b < click_position_scaled[1] < t:
                return True

        return False
