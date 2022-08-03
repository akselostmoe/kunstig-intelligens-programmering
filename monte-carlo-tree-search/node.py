# class for nodes that are used in the tree for MCTS
import numpy as np
import random


class Node:
    def __init__(self, N, parent, state):
        self.N = N  # number of visits
        self.parent = parent
        self.state = state
        self.children = []
        self.eval = 0

    # doing a rollout from the current node, returning the value of the final state at the end of the rollout

    def do_rollout(self, neural_net_lite, copied_board, epsilon):
        # while game is not finished
        while not copied_board.game_over():
            inp = np.expand_dims(np.array(copied_board.state).flatten(), 0)
            action_probabilities = neural_net_lite.predict(inp)[0]
            legal_actions = copied_board.possible_next_states()
            actual_legal_actions = []
            # adding only legal actions to actual_legal_actions
            for a in legal_actions:
                if a != 0.0:
                    actual_legal_actions.append(a)
            actual_action_probabilities = []
            # setting the action porbabilities of illegal moves to 0
            for i in range(len(action_probabilities)):
                if legal_actions[i] == 0.0:
                    action_probabilities[i] = 0.0
                else:
                    actual_action_probabilities.append(action_probabilities[i])
            total_prob = 0
            for i in range(len(actual_action_probabilities)):
                total_prob += actual_action_probabilities[i]
            # re-normalizing legal action probs
            for i in range(len(actual_action_probabilities)):
                actual_action_probabilities[i] = (
                    actual_action_probabilities[i] / total_prob
                )
            best_val = max(actual_action_probabilities)
            # epsilon-greedy
            # exploit
            if random.uniform(0, 1) > epsilon:
                best_index = actual_action_probabilities.index(best_val)
            # explore
            else:
                best_index = random.randint(
                    0, len(actual_action_probabilities) - 1)
            best_action_state = actual_legal_actions[best_index]
            copied_board.update_state(best_action_state)

        # game is finished, returning the value of the final state based on the winner
        if copied_board.winner() == 2:
            return -1
        elif copied_board.winner() == 1:
            return 1
        return 0

    def calculate_q_value(self, child):
        return child.eval / (1 + child.N)

    # method for calculcating Q + u for use in the tree search
    def calculate_tree_policy(self, c, child):
        return self.calculate_q_value(child) + self.exploration_bonus(c, child)

    # helper for exploration bonus
    def exploration_bonus(self, c, child):
        return c * np.sqrt((np.log(self.N)) / (1 + child.N))

    # helper for adding a child to current node
    def add_child(self, child_state):
        child = Node(0, self, child_state)
        self.children.append(child)

    # expanding from current node
    def expand(self, board):
        children_states = board.possible_next_states()
        legal_children_states = []
        for child_state in children_states:
            if child_state != 0.0:
                legal_children_states.append(child_state)
        for child_state in legal_children_states:
            self.add_child(child_state)
