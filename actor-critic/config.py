

# ---------PARAMETER SELECTION-------------
def create_config():

    config_dict = {
        # PIVOTAL PARAMETERS TO USE IN ALL CASES
        "ann_binary": 0,
        "task": 3,
        # Update to see prints for specific episodes
        "episodes_to_visualize": [],

        "actor_decay_rate": 0.9,
        "critic_decay_rate": 0.9,
        "epsilon": 0.9,
        "actor_learning_rate": 0.01,
        "critic_learning_rate": 0.008,
        "actor_discount_factor": 0.9,
        "critic_discount_factor": 0.9,
        # also change episodes to visualize list! Not necessary: Make 1000 for task 3, else 200
        "episodes": 200,
        "max_timesteps": 300,
        # normally 0.005, but can show more convergence on 0.007 on task 1 (but takes longer time)
        "epsilon_decrease": 0.005,
        "layers": [50, 50, 1],  # [50,50,1]

        # EXTRA PIVOTAL PARAMETERS BASED ON TASK
        # TASK 1:
        "L": 0.5,  # [0.1, 1]
        "M_p": 0.1,  # [0.05, 0.5]
        "G": -9.8,  # [-5, -15]
        "tau": 0.02,  # [0.01, 0.1]
        # TASK 2:
        "pegs": 5,  # [3, 5]
        "discs": 6,  # [2, 6]
        # TASK 3:
        "win_probability": 0.8  # [0, 1]
    }
    return config_dict


"""
config_dict = {
        # PIVOTAL PARAMETERS TO USE IN ALL CASES
        "ann_binary": 1,
        "task": 1,
        # Update to see prints for specific episodes
        "episodes_to_visualize": [],

        "actor_decay_rate": 0.9,
        "critic_decay_rate": 0.9,
        "epsilon": 0.9,
        "actor_learning_rate": 0.01,
        "critic_learning_rate": 0.008,
        "actor_discount_factor": 0.9,
        "critic_discount_factor": 0.9,
        "episodes": 200,  # also change episodes to visualize list! Not necessary: Make 1000 for task 3, else 200
        "max_timesteps": 300,
        # normally 0.005, but can show more convergence on 0.007 (but takes longer time)
        "epsilon_decrease": 0.005,
        "layers": [50, 50, 1],  # [50,50,1]

        # EXTRA PIVOTAL PARAMETERS BASED ON TASK
        # TASK 1:
        "L": 0.5,  # [0.1, 1]
        "M_p": 0.1,  # [0.05, 0.5]
        "G": -9.8,  # [-5, -15]
        "tau": 0.02,  # [0.01, 0.1]
        # TASK 2:
        "pegs": 3,  # [3, 5]
        "discs": 4,  # [2, 6]
        # TASK 3:
        "win_probability": 0.8  # [0, 1]
    }
"""

# actor_decay_rate, critic_decay_rate, epsilon, actor_learning_rate, critic_learning_rate,
# actor_discount_factor, critic_discount_factor, ann_binary, episodes, alive_reward, loss_reward

# Table-based critic config for pole balance:
# actor_critic = AC_algorithm(0.9, 0.9, 0.9, 0.01, 0.008, 0.9, 0.9, 0, 200, 3, -100, 1, 300, 0.005)

# NN-based critic for pole balance
# actor_critic = AC_algorithm(0.9, 0.9, 0.9, 0.01, 0.008, 0.9, 0.9, 1, 200, 1, -100, 1, 300, 0.005)

# Table-based critic config for hanoi:
# actor_critic = AC_algorithm(0.9, 0.9, 0.9, 0.01, 0.008, 0.9, 0.9, 0, 200, -0.3, 100, 2, 300, 0.005)

# NN-based critic config for hanoi:
# actor_critic = AC_algorithm(0.9, 0.9, 0.9, 0.01, 0.008, 0.9, 0.9, 1, 200, -0.1, 100, 2, 300, 0.005)

# Table-based critic config for gambler:
# actor_critic = AC_algorithm(0.9, 0.9, 0.9, 0.01, 0.008, 0.9, 0.9, 0, 200, -0.05, 100, 3, 20000, 0.005)

# NN-based critic config for gambler:
# actor_critic = AC_algorithm(0.9, 0.9, 0.9, 0.01, 0.008, 0.9, 0.9, 1, 200, -0.1, 100, 3, 20000, 0.005)
