from .hex_cell import HexCell


class HexBoard:
    def __init__(self, size, starting_player, *copied_state):
        self.size = size
        self.cells = [
            [HexCell(row, column, size, (0, 0)) for column in range(size)]
            for row in range(size)
        ]
        self.current_player = (1, 0) if starting_player == 1 else (0, 1)
        self.state = self.convert_state()
        self.total_board_moves = size**2
        self.player_winner = 0
        self.current_board_move = 0

    # function for updating state on the board
    def update_state(self, next_state):
        index = 1
        for row in range(len(self.cells)):
            for column in range(len(self.cells[row])):
                if self.cells[row][column].value != next_state[index]:
                    self.cells[row][column].update_cell(next_state[index])
                index += 1
        self.state = next_state
        self.current_board_move += 1
        self.current_player = (
            1, 0) if self.current_player == (0, 1) else (0, 1)

    # helper for converting from cells to simple state
    def convert_state(self):
        state = []
        state.append(self.current_player)
        for row in range(len(self.cells)):
            for column in range(len(self.cells[row])):
                state.append(self.cells[row][column].value)
        return state

    # returns a list of state representations for the possible next states, and 0.0 if the action is illegal
    def possible_next_states(self):
        possible_next_states = []
        altered_indices = []
        for i in range(1, self.total_board_moves + 1):
            already_added = False
            if 1 in self.state[i]:
                p_next_state = 0.0
            else:
                p_next_state = [self.current_player]
                for j in range(1, len(self.state)):
                    # checks whether state already have been altered, if the cell is empty or if it already exits in p_next_states
                    if 1 in self.state[j] or already_added or j in altered_indices:
                        # Adds the existing cell if it is occupied or the state has been altered
                        p_next_state.append(self.state[j])
                    else:
                        # assigning the value of current_player to the cell in question
                        p_next_state.append(self.current_player)
                        already_added = True
                        # adds the altered index to know which to stay clear from
                        altered_indices.append(j)
            possible_next_states.append(p_next_state)
        return possible_next_states

    # helper to see if there exist a path through the diagram
    # fmt:off
    def check_for_valid_solution(self):
        # check for player 1
        visited_nodes = []
        first_row = [(0, i) for i in range(self.size)]
        for row, column in first_row:
            root = self.cells[row][column]
            path=[]
            if root.value == (1, 0):
                if self.find_valid_neighbors_player(root, visited_nodes, path):
                    self.player_winner = 1
                    return True
        # check for player 2
        visited_nodes = []
        first_column = [(i, 0) for i in range(self.size)]
        for row, column in first_column:
            root = self.cells[row][column]
            path=[]
            if root.value == (0, 1):
                if self.find_valid_neighbors_player(root, visited_nodes, path):
                    self.player_winner = 2
                    return True
        return False

    # helper for check_for_valid_solution
    def find_valid_neighbors_player(self, root, visited_nodes, path):
        visited_nodes.append(root)
        if root.value == (1, 0):
            path.append(root.placement)
            for neighbor_placement in root.neighbors:
                row, column = neighbor_placement[0], neighbor_placement[1]
                a_cell = self.cells[row][column]
                if a_cell not in visited_nodes and a_cell.value == (1, 0):
                    if row == self.size - 1:
                        path.append(a_cell.placement)
                        return True
                    else:
                        success = self.find_valid_neighbors_player(a_cell, visited_nodes, path)
                        if success:
                            return True
            path.pop()
            return False
        elif root.value==(0, 1):
            path.append(root.placement)
            for neighbor_placement in root.neighbors:
                row, column = neighbor_placement[0], neighbor_placement[1]
                a_cell = self.cells[row][column]
                if a_cell not in visited_nodes and a_cell.value == (0, 1):
                    if column == self.size - 1:
                        path.append(a_cell.placement)
                        return True
                    else:
                        success = self.find_valid_neighbors_player(a_cell, visited_nodes, path)
                        if success:
                            return True
            path.pop()
            return False
        return False

    # fmt: on
    # check if game is finished
    def game_over(self):
        if self.check_for_valid_solution():
            return True
        return False

    # check who has won
    def winner(self):
        finished = self.game_over()
        if finished:
            return self.player_winner
        return False


# static method to get all possible states for oht
def possible_oht_states(state):
    possible_next_states = []
    altered_indices = []
    for i in range(1, (7**2 + 1)):
        already_added = False
        if 1 in state[i]:
            p_next_state = 0.0
        else:
            current_player = (0, 1) if state[0] == (0, 1) else (1, 0)
            p_next_state = [current_player]
            for j in range(1, len(state)):
                # checks whether state already have been altered, if the cell is empty or if it already exits in p_next_states
                if 1 in state[j] or already_added or j in altered_indices:
                    # Adds the existing cell if it is occupied or the state has been altered
                    p_next_state.append(state[j])
                else:
                    # assigning the value of current_player to the cell in question
                    p_next_state.append(current_player)
                    already_added = True
                    # adds the altered index to know which to stay clear from
                    altered_indices.append(j)
        possible_next_states.append(p_next_state)
    return possible_next_states
