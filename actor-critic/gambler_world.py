import random
import numpy as np
import matplotlib.pyplot as plt


class GamblerWorld:
    def __init__(self, win_probability):
        self.units = random.randint(1, 99)
        self.win_probability = win_probability
        self.random_val = random.random()

    def update(self, bet):
        if self.bet_won():
            self.units += int(bet)
        else:
            self.units -= int(bet)

    def bet_won(self):
        self.random_val = random.random()
        if self.random_val <= self.win_probability:
            return True
        else:
            return False

    def convert_state_to_list(self):
        return [self.units]

    def convert_state_to_string(self):
        return str(self.units)

    def possible_actions(self):
        possible_actions = []
        if self.units > 50:
            max_bet = 100 - self.units
        else:
            max_bet = self.units
        for i in range(max_bet):
            possible_actions.append(str(i+1))
        return possible_actions

    def game_over(self):
        if self.units == 100:
            return True
        elif self.units == 0:
            return True
        return False

    def visualize(self, episode_list_state_history,
                  timesteps_reached_list, best_world, actor):
        plot_list = []
        state_map = map(int, list(actor.state_action_table.keys()))
        state_list_int = list(state_map)
        state_list_int.sort()
        for s in state_list_int:
            max_a = 0
            max_v = -np.inf
            for a in actor.state_action_table[str(s)].keys():
                if actor.state_action_table[str(s)][a]["v"] > max_v:
                    max_a = a
                    max_v = actor.state_action_table[str(s)][a]["v"]
            plot_list.append(int(max_a))
        plt.plot(plot_list)
        plt.xlabel("State (units)")
        plt.ylabel("Wager")
        plt.show()
