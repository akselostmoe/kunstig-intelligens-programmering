
import random
# Class for a table-based actor


class Actor:

    def __init__(self, decay_rate, epsilon, learning_rate, discount_factor):
        self.decay_rate = decay_rate
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.episode_state_actions = []
        self.state_action_table = {}

    # check if state is visited before, if not it creates new state-ation pair
    # then chooses the best (epsilon-greedy) next action based on the current policy
    def next_action(self, state, world):
        if len(world.possible_actions()) > 0:
            if state not in self.state_action_table:
                self.state_action_table[state] = {}
                # iterating over the possible actions (all simworlds have a method called possible_actions)
                for a in world.possible_actions():
                    self.state_action_table[state][a] = {
                        "v": 0,
                        "e": 0
                    }

            # take into account the epsilon-greedy explore vs. exploit
            random_val = random.uniform(0, 1)

            # expolit, find the best action from the policy (highest probability)
            if random_val >= self.epsilon:
                best_value = 0
                best_action_index = 0
                iter = 0
                for a in self.state_action_table[state]:
                    if self.state_action_table[state][a]["v"] > best_value:
                        best_value = self.state_action_table[state][a]["v"]
                        best_action_index = iter
                    iter += 1
                return list(self.state_action_table[state].keys())[best_action_index]
            # explore, choose a random action
            else:
                return list(self.state_action_table[state].keys())[random.randint(0, len(list(self.state_action_table[state].keys())) - 1)]
        else:
            return None

    # function for updating eligibilities and values (policy) previously seen in an episode
    def update_vals(self, error):
        # iterating over previously visited state-value pairs in this episode
        for s_a_pair_index in range(len(self.episode_state_actions)):
            s = self.episode_state_actions[s_a_pair_index][0]
            a = self.episode_state_actions[s_a_pair_index][1]

            # going into the table and updating the values and eligibilities
            self.state_action_table[s][a]["v"] = self.state_action_table[s][a]["v"] + \
                self.learning_rate * error * \
                self.state_action_table[s][a]["e"]
            self.state_action_table[s][a]["e"] = self.state_action_table[s][a]["e"] * \
                self.discount_factor * self.decay_rate

    # setting the eligibility to 1 and adding the s-a-pair to list from current episode
    def eligibility_set(self, state, action):
        self.episode_state_actions.append([state, action])
        self.state_action_table[state][action]["e"] = 1

    def episode_reset(self, epsilon_decrease):
        # updating to a smaller epsilon
        self.epsilon = self.epsilon - epsilon_decrease
        # reseting eligibility to zero
        for s in self.state_action_table:
            for a in self.state_action_table[s]:
                self.state_action_table[s][a]["e"] = 0
        # resetting list of s-a-pairs visited in the episode
        self.episode_state_actions = []
