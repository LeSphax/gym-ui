from gym.envs.registration import register

register(
    id='RandomButton-v0',
    entry_point='gym_ui.envs:RandomButton',
)

register(
    id='FixedButton-v0',
    entry_point='gym_ui.envs:FixedButton',
)

register(
    id='FixedButtonHard-v0',
    entry_point='gym_ui.envs:FixedButtonHard',
)