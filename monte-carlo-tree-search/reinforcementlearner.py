import numpy as np
import matplotlib.pyplot as plt
import math

from .hex_board import HexBoard
from .nimboard import NimBoard
from .tree import Tree
from .anet import Anet
from .node import Node
from .litemodel import LiteModel
from .visualizer import Visualizer

# implementing the RL


class RL_algorithm:
    # fmt: off
    def __init__(self, config_dict):
        self.config_dict = config_dict
        # setting parameters from config
        self.episodes = config_dict["episodes"]
        self.simulations = config_dict["simulations"]
        self.layers = config_dict["layers"]
        self.learning_rate = config_dict["learning_rate"]
        self.c = config_dict["c"]
        self.epsilon = config_dict["epsilon"]
        self.epsilon_decay = config_dict["epsilon_decay"]
        self.min_epsilon = config_dict["min_epsilon"]
        self.optimizer = config_dict["optimizer"]
        self.activation = config_dict["activation"]
        self.M = config_dict["M"]
        self.G = config_dict["G"]
        self.save = config_dict["save"]
        self.identifier = config_dict["save_identifier"]
        self.visualize = config_dict["visualize"]
        self.visualize_training_episodes = config_dict["visualize_training_episodes"]
        # NIM specific params:
        self.N = config_dict["N"]
        self.K = config_dict["K"]
        # HEX specific params:
        self.size = config_dict["Size"]

    # the RL algorithm for mcts as described in the spec
    def algorithm(self):
        save_interval = int(math.ceil(self.episodes / (self.M - 1)))
        saved_count = 1
        losses = []
        # initializing ANET
        anet = Anet(self.layers, self.learning_rate, 2*(self.size**2+1), (self.size**2), self.activation, self.optimizer)
        neural_net_lite = LiteModel.from_keras_model(anet.neural_net)
        rbuf_input = []
        rbuf_target = []
        for episode in range(self.episodes):
            # switch who starts between episodes
            player = 1 if episode % 2 == 0 else 2
            print("---------- episode: ", episode + 1,
                  ". player: ", player, "-----------")
            # create a new board at the start of every episode (alternating who is starting)
            actual_board = HexBoard(self.size, player)
            start_state = actual_board.state
            if self.visualize:
                visualizer = Visualizer(self.size)
                visualizer.visualize()
            # creating a new tree with a single root node
            monte_carlo_tree = Tree(Node(0, None, start_state))
            while not actual_board.game_over():
                # monte carlo tree is built based on the number of simulations
                action_node, root, D_list = monte_carlo_tree.monte_carlo_tree_search(
                    self.c, player, self.simulations, neural_net_lite, actual_board, self.epsilon)
                rbuf_input.append(np.array(root.state).flatten().tolist())
                rbuf_target.append(D_list)
                # moving actual_board to next state given from mcts
                if self.visualize and ((episode + 1 in self.visualize_training_episodes) or (self.visualize_training_episodes[0] == -1)):
                    visualizer.action_visualized(player, actual_board.state, action_node.state)
                    visualizer.visualize()
                actual_board.update_state(action_node.state)
                monte_carlo_tree = Tree(action_node)
                player = 2 if player == 1 else 1
            print("winner: ", actual_board.winner())
            # training anet based on batch from rbuf_input and rbuf_target"
            if self.epsilon > self.min_epsilon:
                self.epsilon -= self.epsilon_decay
            history_callback = anet.update_ANN(rbuf_input, rbuf_target)
            losses.append(round(history_callback.history["loss"][0], 3))
            print("losses", losses)
            neural_net_lite = LiteModel.from_keras_model(anet.neural_net)
            if (episode % save_interval == 0 or episode == self.episodes - 1) and self.save:
                anet.save_net(self.identifier, saved_count)
                saved_count += 1
        """
        plt.plot(losses)
        plt.title("losses")
        plt.show()
        """
