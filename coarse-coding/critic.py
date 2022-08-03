from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Input
import tensorflow as tf
import numpy as np


class Critic:

    def __init__(self, params):
        self.alpha = params["learning_rate"]
        self.gamma = params["critic_discount_factor"]
        self.network_dims = params["nn_layers"]
        self.in_dims = params["in_dims"]
        self.model = self.generate_NN(
            self.alpha, self.network_dims, self.in_dims)

    def generate_NN(self, alpha, network_dims=[24], num_inputs=(4,)):
        '''
        Generate neural network with specified parameters. Number of layers are specified in main
        '''
        model = Sequential()
        model.add(Input(shape=(num_inputs,)))
        for layer_size in network_dims:
            # Try with sigmoid
            model.add(Dense(layer_size, activation='sigmoid'))
        model.add(Dense(1, activation="linear"))

        model.compile(optimizer=tf.keras.optimizers.SGD(
            learning_rate=alpha), loss='mse')
        model.summary()
        return model

    def calculate_target(self, reward, next_state, next_action):
        v_s_next = self.evaluate_state(next_state, next_action)
        target = reward + v_s_next*self.gamma
        return target

    def train(self, state, action, target):
        inp = list(np.append(state, action))
        self.model.fit(tf.convert_to_tensor([inp]), target, verbose=0)

    def evaluate_state(self, state, action):
        inp = list(np.append(state, action))
        pred = self.model(tf.convert_to_tensor([inp]))
        return pred

    def get_action(self, state, possible_actions, epsilon):
        best_pred = float("-inf")
        best_action = None
        rand = np.random.rand()
        if np.random.rand() < epsilon:
            return possible_actions[np.random.choice([0, 1, 2])]
        for action in possible_actions:
            inp = list(np.append(state, action))
            pred = self.model(tf.convert_to_tensor([inp])).numpy()
            if pred > best_pred:
                best_pred = pred
                best_action = action
        # print(best_action)
        return best_action
