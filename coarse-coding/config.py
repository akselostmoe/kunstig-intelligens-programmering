# ---------PARAMETER SELECTION-------------
def create_config():
    config_dict = {
        # [-1] = best episode
        "visualize_episodes": [-1],

        # SIMWORLD PARAMS
        "goal_height": 1,
        # n is number of timesteps the force is present
        "n": 4,
        # lenght of poles 1 and 2
        "l_1": 1,
        "l_2": 1,
        # lenght to center of mass of the poles
        "lc_1": 0.5,
        "lc_2": 0.5,
        # mass of poles
        "m_1": 1,
        "m_2": 1,
        # gravity
        "g": 9.8,
        # timestep
        "t": 0.05,

        # ANN PARAMS
        "n_episodes": 2000,
        "max_step": 200,
        "nn_layers": [],
        "in_dims": (6**4)*12+3,
        "learning_rate": 0.01,
        # Discount factor (gamma)
        "critic_discount_factor": 0.90,
        # Epsilon
        "epsilon": 1,
        "epsilon_decay_rate": 0.00,
        # Decay rate (lambda)
        "critic_decay_rate": 0.90,
    }
    return config_dict
