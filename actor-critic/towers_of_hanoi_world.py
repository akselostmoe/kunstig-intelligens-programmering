import matplotlib.pyplot as plt


class TowersOfHanoiWorld:

    def __init__(self, pegs, discs):
        self.total_moves = 0
        # pegs in interval 3 to 5
        self.pegs = pegs
        # disks in interval 2 to 6
        self.discs = discs
        self.state_dict = self.initiate_world()

    # function for creating the world with all disks on one peg
    def initiate_world(self):
        state_dict = {}
        # creating dictinary-keys for all pegs
        for i in range(self.pegs):
            state_dict[i+1] = []
        # putting all disks on first peg
        for i in range(self.discs):
            state_dict[1].append(i+1)
        return state_dict

    # function to make state from dicitonary to string representation
    def convert_state_to_string(self):
        state_string = ""
        for i in range(self.pegs):
            state_string += str(i+1) + "."
            if len(self.state_dict[i+1]) > 0:
                for j in range(len(self.state_dict[i+1])):
                    state_string += str(self.state_dict[i+1][j])
        return state_string

    def convert_state_to_list(self):
        state_list = [0] * (self.pegs * self.discs)
        for i in range(self.pegs):
            for j in range(self.discs):
                possible_index = j + (i * self.discs)
                if len(self.state_dict[i+1]) > j:
                    state_list[possible_index] = self.state_dict[i+1][j]
        return state_list

    def convert_list_to_state(self, list):
        dict = {}
        for i in range(self.pegs):
            dict[i+1] = []
        peg = 0
        for i in range(len(list)):
            if (i) % self.discs == 0:
                peg += 1
            if list[i] > 0:
                dict[peg].append(list[i])
        return dict

    # doing an action and moving the world to another state
    def update(self, action):
        moving_disc = self.state_dict[int(action[0])][0]
        self.state_dict[int(action[0])].remove(moving_disc)
        self.state_dict[int(action[1])].insert(0, moving_disc)

    # returns possible moves in a given state
    def possible_actions(self):
        # making a list with possible actions. each element in the list shows witch peg
        # to move from at index 0 and peg to move to at index 1
        possible_actions = []
        for k in self.state_dict.keys():
            if len(self.state_dict[k]) > 0:
                movable_disc = self.state_dict[k][0]
                for j in self.state_dict.keys():
                    if (len(self.state_dict[j]) == 0) and (not k == j):
                        possible_actions.append(str(k) + str(j))
                    elif (not k == j) and (movable_disc < self.state_dict[j][0]):

                        possible_actions.append(str(k) + str(j))
        return possible_actions

    # check if game is done
    def game_over(self):
        for peg in self.state_dict.keys():
            if peg == 1:
                continue
            if len(self.state_dict[peg]) == self.discs:
                return True
        return False

    # visualizes the state in terminal
    def visualize(self, episode_list_state_history, timesteps_reached_list, best_world, actor):
        if len(episode_list_state_history) > 0:
            for i in range(len(episode_list_state_history)):
                s_dict = self.convert_list_to_state(
                    episode_list_state_history[i])
                print("Timestep: ", i + 1)
                for disc_size in reversed(range(self.discs)):
                    for p in s_dict.keys():
                        if disc_size >= len(s_dict[p]):
                            disc_print = ""
                        else:
                            rev_list = s_dict[p][::-1]
                            disc_print = "=" * rev_list[disc_size]
                        print(
                            f"{disc_print:>{self.discs}}|{disc_print:{self.discs}}", end="")
                    print("")
                print("######################################################")
        else:
            plt.plot(timesteps_reached_list)
            plt.show()
