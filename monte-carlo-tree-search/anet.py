import tensorflow as tf
from tensorflow import keras
import numpy as np


class Anet:
    def __init__(
        self, layers, learning_rate, input_dim, output_dim, activation, optimizer
    ):
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.layers = layers
        self.learning_rate = learning_rate
        self.activation = activation
        self.optimizer = optimizer
        self.neural_net = self.generate_neural_net()

    # creating a new net with cross entropy loss and softmax on the output layer
    def generate_neural_net(self):
        # layers is a list with dimentions of all hidden layers, not including output layer
        model = keras.models.Sequential()
        # adding input layer
        model.add(keras.layers.Input(shape=(self.input_dim,)))
        # adding hidden layers
        for layer_index in range(len(self.layers)):
            model.add(
                keras.layers.Dense(self.layers[layer_index], activation=self.activation)
            )
        # adding softmax output layer
        model.add(keras.layers.Dense(self.output_dim, activation="softmax"))
        # checking the optimizr defined in config
        if self.optimizer == "adam":
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate),
                loss=keras.losses.KLDivergence(),
            )
        elif self.optimizer == "sgd":
            model.compile(
                optimizer=keras.optimizers.SGD(learning_rate=self.learning_rate),
                loss=keras.losses.KLDivergence(),
            )
        elif self.optimizer == "rmsprop":
            model.compile(
                optimizer=keras.optimizers.RMSprop(learning_rate=self.learning_rate),
                loss=keras.losses.KLDivergence(),
            )
        else:  # adagrad
            model.compile(
                optimizer=keras.optimizers.Adagrad(learning_rate=self.learning_rate),
                loss=keras.losses.KLDivergence(),
            )
        return model

    # function for fitting network
    def update_ANN(self, state, target):
        return self.neural_net.fit(state, target, batch_size=1)

    # takes in a state in list format and uses help function to make it into tensor
    def forward(self, state):
        return self.neural_net(tf.expand_dims(np.array(state).flatten(), axis=0))

    def list_to_tensor(self, state_list):
        return tf.convert_to_tensor(state_list)

    # saving the neural net in folder. Unique foler name is given to the run,
    # and exact model is named after the episode in the run
    def save_net(self, identifier, episode):
        self.neural_net.save(f"./exercise 2/code/saved_anets/{identifier}/{episode}")


# static model that returns a list of all previously saved ANETs from a run
def load_net(identifier, M):
    nets_from_a_run = []
    # for all saved nets in a run, load them back up again
    for i in range(M):
        try:
            net = keras.models.load_model(
                f"./exercise 2/code/saved_anets/{identifier}/{i+1}"
            )
            nets_from_a_run.append(net)
        except:
            pass
    return nets_from_a_run
