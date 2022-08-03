import matplotlib.pyplot as plt
import math


class Visualizer:
    def __init__(self, size):
        self.size = size
        self.table_colors = ["black", "white"]
        self.player_colors = ["lightblue", "navy"]
        # interactive mode on
        plt.ion()
        plt.axis("off")
        self.board_dict = self.create_blank_board()

    def move_values(self, values, move_factor):
        new_values = []
        for val in values:
            new_values.append(val + move_factor)
        return new_values

    # creating only the board without players choices (blank board)
    def create_blank_board(self):
        horisontal_values = [0, 0.5, 1, 1, 0.5, 0, 0]
        vertical_values = [0, 0.5, 0, -0.75, -1.25, -0.75, 0]
        # dictionary with row number as key, and all spots in row as a 2d list per key
        board = {}
        for row in range(self.size):
            horisontal_values = self.move_values(horisontal_values, -0.5)
            vertical_values = self.move_values(vertical_values, -1.25)
            for col in range(self.size):
                next_h_val = self.move_values(horisontal_values, (0.5 * col))
                next_v_val = self.move_values(vertical_values, (-1.25 * col))
                new_spot = [
                    next_h_val,
                    next_v_val,
                    self.table_colors[0],
                    self.table_colors[1],
                ]
                if col == 0:
                    board[row] = [new_spot]
                else:
                    board[row].append(new_spot)
        return board

    def visualize(self):
        for k in self.board_dict.keys():
            for element in self.board_dict[k]:
                plt.plot(element[0], element[1], color=element[2])
                plt.fill(element[0], element[1], element[3])
        plt.title("Player one = light blue\nPlayer two = dark blue")
        plt.pause(0.1)

    def action_visualized(self, player, new_state, old_state):
        for i in range(1, len(new_state)):
            if new_state[i] != old_state[i]:
                action_index = i - 1
        row = math.floor(action_index / self.size)
        col = action_index % self.size
        if player == 2:
            self.board_dict[row][col][3] = self.player_colors[1]
        else:
            self.board_dict[row][col][3] = self.player_colors[0]
