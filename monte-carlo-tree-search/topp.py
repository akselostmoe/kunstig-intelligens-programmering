import numpy as np
import matplotlib.pyplot as plt

from .anet import Anet
from .anet import load_net
from .nimboard import NimBoard
from .hex_board import HexBoard
from .visualizer import Visualizer


class Topp:
    # fmt:off
    def __init__(self, config_dict):
        # HEX params:
        self.size = config_dict["Size"]
        # neural net params
        self.layers = config_dict["layers"]
        self.learning_rate = config_dict["learning_rate"]
        self.input_dim = 2*(self.size**2+1)
        self.output_dim = (self.size**2)
        self.optimizer = config_dict["optimizer"]
        self.activation = config_dict["activation"]
        self.visualize = config_dict["visualize"]
        self.visualize_topp_games = config_dict["visualize_topp_games"]
        # Topp params
        self.M = config_dict["M"]
        self.G = config_dict["G"]
        self.identifier = config_dict["save_identifier"]
        self.agents = []
        # loading a list of agents that are going to be in TOPP
        nets = load_net(self.identifier, self.M)
        for net in nets:
            agent = Anet(self.layers, self.learning_rate, self.input_dim,
                         self.output_dim, self.activation, self.optimizer)
            # setting the net of the agent to be a loaded net
            agent.neural_net = net
            self.agents.append(agent)

    def tournament(self):
        # play_tournament_games i k
        # making two lists with 0 for every value mapping to each agent
        agent_wins = [0 for i in range(len(self.agents))]
        agent_games = [0 for i in range(len(self.agents))]
        # double for loop to create matches between all players
        for home_player in range(len(self.agents) - 1):
            for away_player in range(home_player + 1, len(self.agents)):
                # play series between two players
                wins = self.series(self.agents[home_player], self.agents[away_player])
                # update played games and wins for agents
                agent_wins[home_player] += wins[0]
                agent_wins[away_player] += wins[1]
                agent_games[home_player] += self.G
                agent_games[away_player] += self.G
        y_pos = np.arange(1,len(agent_wins) + 1)
        plt.close("all")
        plt.bar(y_pos, agent_wins, align='center', alpha=0.5)
        plt.title("Number of wins per agent")
        plt.show()
        print("game wins per agent: ", agent_wins, "\ngames played per agent: ", agent_games)
        return agent_wins, agent_games

    # playing the G games between two actors to make one series

    def series(self, agent_1, agent_2):
        a_1_wins = 0
        a_2_wins = 0
        for game in range(self.G):
            player = 1 if game % self.G == 0 else 2
            turn  = 0 if game % 2 == 0 else 1
            board = HexBoard(self.size, player)
            if self.visualize:
                visualizer = Visualizer(self.size)
            while not board.game_over():
                distribution = []
                if turn % 2 == 0:
                    player = 1
                    distribution = agent_1.forward(board.state).numpy()[0]
                else:
                    player = 2
                    distribution = agent_2.forward(board.state).numpy()[0]
                possible_states = board.possible_next_states()
                # find indices for illegal states
                illegal_indices = []
                for i in range(len(distribution)):
                    if possible_states[i] == 0.0:
                        illegal_indices.append(i)
                new_distribution = np.delete(distribution, illegal_indices)
                for index in sorted(illegal_indices, reverse=True):
                    del possible_states[index]
                # extracting the three best moves and uses their probability to pick the one of them
                if len(new_distribution) > 2:
                    top_contenders_indecies = np.argpartition(new_distribution, -3)[-3:]
                    top_contenders=new_distribution[(top_contenders_indecies)]
                    normalized_distribution = top_contenders/sum(top_contenders)
                    action = np.random.choice(top_contenders, 1, p=normalized_distribution)
                    distribution_list = new_distribution.tolist()
                    action_index = distribution_list.index(action)
                elif len(new_distribution) > 1:
                    top_contenders_indecies = np.argpartition(new_distribution, -2)[-2:]
                    top_contenders=new_distribution[(top_contenders_indecies)]
                    normalized_distribution = top_contenders/sum(top_contenders)
                    action = np.random.choice(top_contenders, 1, p=normalized_distribution)
                    distribution_list = new_distribution.tolist()
                    action_index = distribution_list.index(action)
                else:
                    action_index = np.argmax(new_distribution)
                # action_index = np.argmax(new_distribution)
                next_state = possible_states[action_index] 
                # print(next_state)
                if self.visualize and ((game + 1 in self.visualize_topp_games) or (self.visualize_topp_games[0] == -1)):
                    visualizer.action_visualized(player, board.state, next_state) 
                    visualizer.visualize() 
                board.update_state(next_state)
                turn += 1
            if board.winner() == 1:
                a_1_wins+=1
            else:
                a_2_wins+=1
        return [a_1_wins, a_2_wins]
