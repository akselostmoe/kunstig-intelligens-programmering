
import numpy as np
import copy
import matplotlib.pyplot as plt
from config import create_config


class Acrobat:

    def __init__(self, params):
        self.theta_1 = 0.0
        self.theta_1_der = 0.0
        self.theta_2 = 0.0
        self.theta_2_der = 0.0
        self.goal_height = params["goal_height"]
        # n is number of timesteps the force is present
        self.n = params["n"]
        # lenght of poles 1 and 2
        self.l_1 = params["l_1"]
        self.l_2 = params["l_2"]
        # lenght to center of mass of the poles
        self.lc_1 = params["lc_1"]
        self.lc_2 = params["lc_2"]
        # mass of poles
        self.m_1 = params["m_1"]
        self.m_2 = params["m_2"]
        # gravity
        self.g = params["g"]
        # timestep
        self.t = params["t"]
        # state rep
        self.state = [self.theta_1, self.theta_1_der,
                      self.theta_2, self.theta_2_der]
        # coordinates (fixed) of upper pivot
        self.x_p1 = 0.0
        self.y_p1 = 0.0
        # start coordinates of lower pivot and tip of pole 2
        self.x_p2 = self.x_p1 + self.l_1 * np.sin(self.theta_1)
        self.y_p2 = self.y_p1 - self.l_1 * np.cos(self.theta_1)
        self.x_tip = self.x_p2 + self.l_2 * np.sin(self.theta_1 + self.theta_2)
        self.y_tip = self.y_p2 - self.l_2 * np.cos(self.theta_1 + self.theta_2)
        self.all_states_in_episode = [
            ([self.x_p1, self.x_p2], [self.y_p1, self.y_p2], [self.x_p2, self.x_tip], [self.y_p2, self.y_tip])]
        self.num_distribution = {}

    def update_state(self, B, steps):
        # force
        f = self.action_to_force(B)
        final_count = 0
        for i in range(self.n):

            # calculating intermidiate terms
            o_2 = self.m_2 * self.lc_2 * self.g * \
                np.cos(self.theta_1 + self.theta_2 - (np.pi / 2))
            o_1 = - self.m_2 * self.l_1 * self.lc_2 * (self.theta_2_der ** 2) * np.sin(self.theta_2) - 2 * self.m_2 * self.l_1 * self.lc_2 * self.theta_2_der * \
                self.theta_1_der * np.sin(self.theta_2) + (self.m_1 * self.lc_1 +
                                                           self.m_2 * self.l_1) * self.g * np.cos(self.theta_1 - (np.pi / 2)) + o_2
            d_2 = self.m_2 * ((self.lc_2 ** 2) + self.l_1 *
                              self.lc_2 * np.cos(self.theta_2)) + 1
            d_1 = self.m_1 * (self.lc_1 ** 2) + self.m_2 * ((self.l_1 ** 2) +
                                                            (self.lc_2 ** 2) + 2 * self.l_1 * self.lc_2 * np.cos(self.theta_2)) + 2

            theta_2_second_der = ((self.m_2 * (self.lc_2 ** 2) + 1 - ((d_2 ** 2) / d_1)) ** -1) * (f + (
                d_2 / d_1) * o_1 - self.m_2 * self.l_1 * self.lc_2 * (self.theta_1_der ** 2) * np.sin(self.theta_2) - o_2)
            theta_1_second_der = - (d_2 * theta_2_second_der + o_1) / d_1

            # euler method
            self.theta_2_der = self.theta_2_der + self.t * theta_2_second_der
            self.theta_1_der = self.theta_1_der + self.t * theta_1_second_der
            self.theta_2 = self.theta_2 + self.t * self.theta_2_der
            self.theta_1 = self.theta_1 + self.t * self.theta_1_der

            if self.theta_1 < 0:
                self.theta_1 = (self.theta_1 % (-2*np.pi))
            else:
                self.theta_1 = self.theta_1 % (2*np.pi)
            if self.theta_2 < 0:
                self.theta_2 = (self.theta_2 % (-2*np.pi))
            else:
                self.theta_2 = self.theta_2 % (2*np.pi)

            # updating coordinates of lower pivot and tip of pole 2
            self.x_p2 = self.x_p1 + self.l_1 * np.sin(self.theta_1)
            self.y_p2 = self.y_p1 - self.l_1 * np.cos(self.theta_1)
            self.x_tip = self.x_p2 + self.l_2 * \
                np.sin(self.theta_1 + self.theta_2)
            self.y_tip = self.y_p2 - self.l_2 * \
                np.cos(self.theta_1 + self.theta_2)
            self.all_states_in_episode.append(
                ([self.x_p1, self.x_p2], [self.y_p1, self.y_p2], [self.x_p2, self.x_tip], [self.y_p2, self.y_tip]))

            if self.is_final():
                final_count += 1
        self.state = [self.theta_1, self.theta_1_der,
                      self.theta_2, self.theta_2_der]
        if final_count > 0:
            return 100
        else:
            return -1

    # helper for making action rep into force
    def action_to_force(self, action):
        if action == [0, 0, 1]:
            return 1
        elif action == [0, 1, 0]:
            return 0
        else:
            return -1

    def create_state_rep(self):
        pass

    def get_actions(self):
        # 1, 0, -1
        return [[0, 0, 1], [0, 1, 0], [1, 0, 0]]

    def is_final(self):
        if self.y_tip >= self.goal_height:
            return True
        return False

    # convert to a coarse code state rep
    def get_state(self, filters):
        return self.coarse_code(filters)

    def get_best_result(self):
        pass

    """
    def num_step(self, steps):
        self.step_history.append(steps)
    """

    def is_best(self, steps):
        pass

    def visualize_current_episode(self):
        # bruke visualizer og listen med states i episoden
        pass

    def coarse_code(self, filters):
        '''
        State on the format: [Angle 1 (float), Angle speed 1 (float), Angle 2 (float), Angle speed 2 (float)]
        Filter example: array([[-2. , -1. ,  0. ,  1. ,  2. ], [ 5. , -1. ,  0. ,  1. ,  5. ], [ 0. ,  1. ,  2. ,  3. ,  4. ],[-2. , -1.5,  0. ,  1.5,  2. ]]),
                        array([[-2.63356217, -1.63356217, -0.63356217,  0.36643783,  1.36643783], [ 4.36643783, -1.63356217, -0.63356217,  0.36643783,  4.36643783],
                              [-0.63356217,  0.36643783,  1.36643783,  2.36643783,  3.36643783], [-2.63356217, -2.13356217, -0.63356217,  0.86643783,  1.36643783]])
        Multiple filters in order to further separate
        '''
        inds = []
        for filter in filters:
            ind = ''
            for i in range(len(self.state)):
                var = self.state[i]
                for j in range(len(filter[i])):
                    if var <= filter[i][j]:
                        ind += str(j)
                        break
                    elif var > filter[i][-1]:
                        ind += str(len(filter[i]))
                        break
            num = 0
            for k in range(len(ind)):
                num += int(ind[k])*6**k
            one_hot = np.zeros(1296)
            one_hot[num] = 1
            inds.append(one_hot)

            # print("State in number: %s" % (num))

            if num in self.num_distribution:
                self.num_distribution[num] += 1
            else:
                self.num_distribution[num] = 1
            # print("State in number: %s" % (num))

        return list(np.array(inds).flatten())

    @staticmethod
    def visualize_best_episode():
        pass

    @staticmethod
    def create_filters(num_filters=11, base_filter=np.array([[-np.pi, -0.5*np.pi, 0, 0.5*np.pi, np.pi],
                                                             [-4*np.pi, -2*np.pi,
                                                                 0, 2*np.pi, 4*np.pi],
                                                             [-np.pi, -0.5*np.pi,
                                                                 0, 0.5*np.pi, np.pi],
                                                             [-9*np.pi, -4.5*np.pi, 0, 4.5*np.pi, 9*np.pi]])):
        filters = [base_filter]
        for i in range(num_filters):
            offset = np.random.uniform(-np.pi, np.pi)
            new_filter = base_filter+offset
            filters.append(new_filter)
        return filters
