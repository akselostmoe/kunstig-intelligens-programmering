# ---------PARAMETER SELECTION-------------
def create_config():

    config_dict = {
        "run_mcts": False,
        "run_topp": True,
        "episodes": 45,
        "simulations": 10,
        # Only hidden layers, not input or output
        # [64, 128, 256, 64],  # [128, 256, 512, 256, 128],
        "layers": [64, 128, 256, 64],
        "learning_rate": 0.005,
        "c": 1,
        "epsilon": 1.2,
        "epsilon_decay": 0.0075,
        "min_epsilon": 0.2,
        "optimizer": "sgd",  # adagrad, sgd, rmsprop, adam. all in small letters
        "activation": "relu",  # linear, sigmoid, tanh, relu
        "M": 5,  # number of agents to be used in TOPP, and times saved
        "G": 20,  # games to be played per match between ANETS in TOPP
        "save": False,  # boolean variable to tell if nets should be saved during the run
        "save_identifier": "test",  # for 5 x 5 demo use "test"
        "visualize": False,
        # -1 as only element in list = all episodes are visualized
        "visualize_training_episodes": [1],
        "visualize_topp_games": [1, 2],
        # NIM specific parameters
        "N": 16,
        "K": 6,
        # hex-parameters
        "Size": 5,  # 3-10
    }
    return config_dict


def get_oht_config():
    config_dict = {
        "identifier": "martin",
        "last_net": 4,
        "learning_rate": 0.005,
        "optimizer": "sgd",  # endre
        "activation": "relu",
        "layers": [64, 128, 256, 64],
    }
    return config_dict


# ====== 5 x 5 params under =========
"""
config_dict = {
        "run_mcts": False,
        "run_topp": True,
        "episodes": 5,
        "simulations": 10,
        # Only hidden layers, not input or output
        "layers": [64, 128, 128, 64],
        "learning_rate": 0.01,
        "c": 1,
        "epsilon": 0.6,
        "epsilon_decay": 0.01,
        "optimizer": "sgd",  # adagrad, sgd, rmsprop, adam. all in small letters
        "activation": "relu",  # linear, sigmoid, tanh, relu
        "M": 5,  # number of agents to be used in TOPP, and times saved
        "G": 2,  # games to be played per match between ANETS in TOPP
        "save": False,  # boolean variable to tell if nets should be saved during the run
        "times_saved": 5,  # amount of times to save ANETs during a run
        "save_identifier": "test",
        "visualize": True,
        # -1 as only element in list = all episodes are visualized
        "visualize_training_episodes": [-1],
        "visualize_topp_games": [1, 2],
        # NIM specific parameters
        "N": 16,
        "K": 6,
        # hex-parameters
        "Size": 5,  # 3-10
    }
    return config_dict
"""
