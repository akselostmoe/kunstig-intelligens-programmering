# implementing a critic that evaluates states (not state-action pairs)
import tensorflow as tf
from tensorflow import keras

import math
import numpy as np


class Critic:
    def __init__(self, decay_rate, learning_rate, discount_factor, ann_binary, input_dims, layers):
        self.decay_rate = decay_rate
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.ann_binary = ann_binary
        self.input_dims = input_dims
        self.layers = layers
        self.state_table = {}
        self.episode_states = []
        self.neural_net = self.generate_neural_net(
            self.layers, self.learning_rate)

    def generate_neural_net(self, layers_list, l_rate, act="relu", opt="SGD"):
        # layers_list is a list with dimentions of all hidden layers, not including output layer
        model = keras.models.Sequential()
        # adding input layer
        model.add(keras.layers.Input(shape=(self.input_dims,)))
        # adding hidden layers
        for layer_index in range(len(layers_list)-1):
            model.add(keras.layers.Dense(
                layers_list[layer_index], activation=act))
        # adding output layer
        model.add(keras.layers.Dense(self.layers[-1]))
        model.compile(optimizer=keras.optimizers.SGD(
            learning_rate=l_rate), loss='mse')
        # print(model.summary())
        return model

    # function for updating eligibilities and values previously seen in an episode
    # or using the neural net to update
    def update_vals(self, error, target, list_state, timestep):
        if not self.ann_binary:
            for s in self.episode_states:
                self.state_table[s]["v"] = self.state_table[s]["v"] + \
                    self.learning_rate * error * \
                    self.state_table[s]["e"]
                self.state_table[s]["e"] = self.state_table[s]["e"] * \
                    self.discount_factor * self.decay_rate
        elif timestep % 5 == 0:
            self.update_ANN(list_state, target)

    # function for fitting network
    def update_ANN(self, state, target):
        self.neural_net.fit(tf.expand_dims(
            self.list_to_tensor(state), axis=0), target, verbose=0)

    def forward(self, state):
        # takes in a state in list format and uses help function to make it into tensor
        return self.neural_net(tf.expand_dims(self.list_to_tensor(state), axis=0))

    def calculate_td_error(self, state, next_state, reward):
        # check if the state is seen previously, if not set value to zero
        if next_state not in self.state_table:
            self.state_table[next_state] = {"v": 0}
        td_error = reward + self.discount_factor * \
            self.state_table[next_state]["v"] - \
            self.state_table[state]["v"]
        return td_error

     # setting the eligibility to 1 and adding the state to list from current episode
    def eligibility_set(self, state):
        self.episode_states.append(state)
        if state not in self.state_table:
            self.state_table[state] = {"v": 0, "e": 1}
        else:
            self.state_table[state]["e"] = 1

    def episode_reset(self):
        # reseting eligibility to zero
        for s in self.state_table:
            self.state_table[s]["e"] = 0
        # resetting list of states visited in the episode
        self.episode_states = []

    def list_to_tensor(self, state_list):
        return tf.convert_to_tensor(state_list)

    def get_target_value(self, reward, next_state):
        return reward + self.discount_factor * self.forward(next_state)
