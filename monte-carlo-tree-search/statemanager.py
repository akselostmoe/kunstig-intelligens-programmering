# file with the state managers for both Nim and Hex

class StateManagerNim:

    def __init__(self):
        pass

    # doing an action on the board
    def do_action(self, next_state, nimboard):
        nimboard.update_state(next_state)

    # check to see if the game is in a finished state, if so returns true

    def game_over(self, nimboard):
        if nimboard.game_over():
            return True
        return False

    # returns the winner of the game if game is finished, else returns false
    def winner(self, nimboard):
        if self.game_over(nimboard):
            return nimboard.state[0]
        return False


class StateManagerHex:

    def __init__(self):
        pass

    def do_action(self, state):
        pass
