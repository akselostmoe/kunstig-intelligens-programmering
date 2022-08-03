

class NimBoard:

    def __init__(self, N, K):
        self.N = N
        self.K = K
        self.total_board_moves = K
        # state is represented as a list with the first element being the player who has the turn,
        # and the rest of the list being of N lenght, where all elements are 0 but the element on the index (+1)
        # of the number of pieces left

        # player one starts
        self.state = [1]
        # adding the rest of the state
        for i in range(self.N):
            if i != (N - 1):
                self.state.append(0)
            else:
                self.state.append(1)

    # function for updating state on the board, called by the Nim state manager
    def update_state(self, next_state):
        self.state = next_state

    # helper for creating state representation

    def create_state_representation(self, player, pieces_left):
        state_rep = []
        state_rep.append(player)
        for i in range(self.N):
            if i == (pieces_left - 1):
                state_rep.append(1)
            else:
                state_rep.append(0)
        return state_rep

    # checking if move is legal
    def check_legal_moves(self):
        pieces_left = self.state[1:].index(1) + 1
        legal_next_states = self.possible_next_states()
        if pieces_left > self.K:
            return legal_next_states
        else:
            legal_states = []
            for i in range(pieces_left - 1):
                legal_states.append(legal_next_states[i])
            return legal_states

    # returns a list of state representations for the possible next states

    def possible_next_states(self):
        pieces_left = self.state[1:].index(1) + 1
        possible_next_states = []
        for i in range(self.K):
            # adding the next player to the start of the next state
            if self.state[0] == 1:
                next_player = 2
            else:
                next_player = 1
            if (pieces_left - (i + 1)) > 0:
                possible_next_states.append(self.create_state_representation(
                    next_player, pieces_left - (i + 1)))

        return possible_next_states

    """
    # returning a list of possible moves from the current state
    def possible_moves(self):
        pieces_left = self.state[1:].index(1) + 1
        possible_moves = []
        for i in range(self.K):
            if (pieces_left - (i + 1)) > 0:
                possible_moves.append(pieces_left - (i + 1))

        return possible_moves
    """

    # check if game is finished, (and who has won?)
    # the player that removes the last piece is the loser
    def game_over(self):
        if self.state[1] != 0:
            return True
        return False
    # check who has won

    def winner(self):
        if self.game_over():
            if self.state[0] == 1:
                return 2
            else:
                return 1
        return False

    def visualize(self):
        pass


"""
nim = NimBoard(4, 5)
print(nim.state)
# print(nim.possible_moves())
print("possible moves: ", nim.possible_next_states())
print("legal moves: ", nim.check_legal_moves())
"""
