from gym.envs.registration import register
register(
    id='RlTracking-v0',
    entry_point='rl_tracking.envs:RlTracking',
    max_episode_steps=200   #tshh
)