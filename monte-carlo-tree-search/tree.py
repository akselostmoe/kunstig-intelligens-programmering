# Class for the tree to be used in the MCTS
import numpy as np
import copy
import random


class Tree:
    # fmt: off
    def __init__(self, root_node):
        self.root_node = root_node

    # evaluate given the tree policy for each node given as input. Returning the leaf node based on current policy
    def tree_search(self, start_player, c, board):
        if start_player == 1:
            turn = 0
        else:
            turn = 1
        iter_root_node = self.root_node
        # while not in a leaf node
        while len(iter_root_node.children) > 0:
            # maximize player
            if turn % 2 == 0:
                max_val = -np.inf
                max_child = None
                # iterating over children on a given node, ending each for loop with the child with the max value edge to the current node
                for child in iter_root_node.children:
                    if iter_root_node.calculate_tree_policy(c, child) >= max_val:
                        max_val = iter_root_node.calculate_tree_policy(
                            c, child)
                        max_child = child
                iter_root_node = max_child
            # minimize player
            else:
                min_val = np.inf
                min_child = None
                # iterating over children on a given node, ending each for loop with the child with the min value edge to the current node
                for child in iter_root_node.children:
                    if iter_root_node.calculate_tree_policy(-c, child) <= min_val:
                        min_val = iter_root_node.calculate_tree_policy(
                            -c, child)
                        min_child = child
                iter_root_node = min_child
            if iter_root_node is not None:
                board.update_state(iter_root_node.state)
            turn += 1
        return iter_root_node

    # set a new root node (pruning the tree)
    def set_root_node(self, node):
        self.root_node = node
        node.parent = None

    def backprop(self, node, final_value):
        # starting backprop from the leaf_node from the tree policy (node inputed to the function)
        # final value inputed is the returned value form the rollout (-1 or 1)
        while node.parent:
            node.N += 1
            node.eval += final_value
            node = node.parent
        # adding to N of the root node after while loop
        node.N += 1

    # function that does the tree search, rollout from leaf-node, and then backprop
    # before pruning the tree to have the best child of the root node as the new root
    def monte_carlo_tree_search(self, c, player, simulations, anet, board, epsilon):
        for i in range(simulations):
            mc_board = copy.deepcopy(board)
            leaf_node = self.tree_search(player, c, mc_board)
            # checking if the leaf node has been visited before, if not, then rollout on leaf node
            if leaf_node.N > 0 and not mc_board.game_over():
                leaf_node.expand(mc_board)
                # choose randomly one of the expanded nodes from the previous leaf node
                random_index = random.randint(0, len(leaf_node.children) - 1)
                leaf_node = leaf_node.children[random_index]
            # perform rollout
            final_value = leaf_node.do_rollout(anet, mc_board, epsilon)
            # backprop the final value
            self.backprop(leaf_node, final_value)

        # pruning the tree and making the best child of the root node the new root node
        best_child = None
        children_N_list = []
        total_children_visits = 0
        val = 0
        child_counter = 0
        possible_next_states = board.possible_next_states()
        # adding number of visits of all legal children til children_N_list
        # finding the child with the most visits (best_child)
        for i in range(len(possible_next_states)):
            if possible_next_states[i] != 0.0:
                children_N_list.append(self.root_node.children[child_counter].N)
                total_children_visits += self.root_node.children[child_counter].N
                if self.root_node.children[child_counter].N >= val:
                    val = self.root_node.children[child_counter].N
                    best_child = self.root_node.children[child_counter]
                child_counter += 1
            else:
                children_N_list.append(0.0)
        # normalize the amount of visits to each child of the root
        norm_children_N_list = []
        # norm_children_N_list is going to become the probability distribution D
        for el in children_N_list:
            norm_children_N_list.append(el/total_children_visits)
        # the returned node is the node to go along with D as input for the ANET
        returned_root_node = self.root_node
        # pruning tree
        self.set_root_node(best_child)
        return best_child, returned_root_node, norm_children_N_list


