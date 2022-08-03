from hashlib import new
from importlib.metadata import distribution
import tensorflow as tf
from tensorflow import keras
import numpy as np

from .anet import Anet
from .config import get_oht_config
from .hex_board import possible_oht_states


class HexActor:
    # fmt:off
    def __init__(self):
        config_dict = get_oht_config()
        self.layers = config_dict["layers"]
        self.learning_rate = config_dict["learning_rate"]
        self.input_dim = 2*(7**2+1)
        self.output_dim = (7**2)
        self.activation = config_dict["activation"]
        self.optimizer = config_dict["optimizer"]
        self.agent = self.load_best_net(config_dict["identifier"], config_dict["last_net"])
        

    def get_action(self, state):
        correct_format_state = []
        for el in state:
            if el == 1:
                correct_format_state.append((1,0))
            elif el == 2:
                correct_format_state.append((0,1))
            else:
                correct_format_state.append((0,0))
        possible_states = possible_oht_states(correct_format_state)
        distribution = self.agent.forward(correct_format_state).numpy()[0]
        illegal_indices = []
        for i in range(len(distribution)):
            if possible_states[i] == 0.0:
                illegal_indices.append(i)
        new_distribution = np.delete(distribution, illegal_indices)
        for index in sorted(illegal_indices, reverse=True):
            del possible_states[index]
        best_state = possible_states[np.argmax(new_distribution)]
        row, col = 0, 0
        row_counter = -1
        for i in range(1, len(best_state)):
            row_counter+=1
            if row_counter >= 7:
                row += 1
                row_counter = 0
            if best_state[i]!=correct_format_state[i]:
                col = (i-1) % 7
                break
        return row, col
                 

    def load_best_net(self, identifier, best_net):
        agent = Anet(self.layers, self.learning_rate, self.input_dim, self.output_dim, self.activation, self.optimizer)
        net = keras.models.load_model(f"./exercise 2/code/saved_anets/{identifier}/{best_net}")
        agent.neural_net = net
        return agent
