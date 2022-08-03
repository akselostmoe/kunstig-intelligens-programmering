
import random
import numpy as np
import matplotlib.pyplot as plt


class PoleBalancingWorld:

    def __init__(self, L, M_p, G, tau):
        self.L = L
        self.M_p = M_p
        self.G = G
        self.tau = tau
        self.M_c = 1
        self.F = 10
        self.theta_max = 0.21
        self.x_min = -2.4
        self.x_max = 2.4
        self.first_der_x = 0
        self.second_der_x = 0
        self.second_der_theta = 0
        self.x = 0
        self.first_der_theta = 0
        self.theta = random.random() * self.theta_max * 2 - self.theta_max
        self.theta_history = [self.theta]

    # doing all the computations as shown in the formulas in the pdf
    def update_per_timestep(self, B):
        self.second_der_theta = self.helper_second_der_theta(B)
        self.second_der_x = self.helper_second_der_x(B)
        self.first_der_theta = self.first_der_theta + self.tau * self.second_der_theta
        self.first_der_x = self.first_der_x + self.tau * self.second_der_x
        self.theta = self.theta + self.tau * self.first_der_theta
        self.x = self.x + self.tau * self.first_der_x
        self.theta_history.append(self.theta)

    # functions for checking if the game is lost or won
    def game_over(self):
        if np.abs(self.theta) > self.theta_max:
            return True
        return False

    # return a list of possible actions to take
    def possible_actions(self):
        return ["0", "1"]

    # helpers for the formulas for second derivatives of theta and x

    def helper_second_der_theta(self, B):
        return (self.G * np.sin(self.theta) + (np.cos(self.theta) * (-B - self.M_p * self.L * (self.first_der_theta ** 2) * np.sin(self.theta))) / (self.M_p + self.M_c)) / (self.L * ((4 / 3) - (self.M_p * (np.cos(self.theta) ** 2)) / (self.M_p + self.M_c)))

    def helper_second_der_x(self, B):
        return (B + self.M_p * self.L * ((self.first_der_theta ** 2) * np.sin(self.theta) - self.second_der_theta * np.cos(self.theta))) / (self.M_p + self.M_c)

    # converting the state-variables to a string representation for table based
    def convert_state_to_string(self):
        # value of x and theta is separated into 8 different bins
        theta_bins = [-self.theta_max, -self.theta_max * 0.75, -self.theta_max * 0.5, -self.theta_max *
                      0.25, 0.0, self.theta_max * 0.25, self.theta_max * 0.5, self.theta_max * 0.75, self.theta_max]
        string_theta_bin = str(np.digitize(self.theta, theta_bins))
        der_bins = [-2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0]
        string_x_first_der_bin = str(np.digitize(self.first_der_x, der_bins))
        string_theta_first_der_bin = str(
            np.digitize(self.first_der_theta, der_bins))
        return string_theta_bin + string_x_first_der_bin + string_theta_first_der_bin

    # ann state converter
    def convert_state_to_list(self):
        return [self.x, self.theta, self.first_der_x, self.first_der_theta]

    def visualize(self, episode_list_state_history, timesteps_reached_list, best_world, actor):
        if len(episode_list_state_history) > 0:
            plt.plot(self.theta_history)
        else:
            fig, axes = plt.subplots(ncols=2, nrows=1)
            axes[0].plot(timesteps_reached_list)
            if not (isinstance(best_world, int)):
                axes[1].plot(best_world.theta_history)
        plt.show()
