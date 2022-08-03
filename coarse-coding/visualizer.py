import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Visualizer:
    def __init__(self, data, goal_height):
        self.data = data
        self.goal_height = goal_height
        self.x_vals_3 = [-10, 10]
        self.y_vals_3 = [self.goal_height, self.goal_height]
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set(xlim=(-3, 3), ylim=(-3, 3))
        self.fig = fig
        self.ax = ax
        self.line_1 = self.ax.plot(
            self.data[0][0], self.data[0][1], 'bo', linestyle="solid")[0]
        self.line_2 = self.ax.plot(
            self.data[0][2], self.data[0][3], 'bo', linestyle="solid")[0]
        self.line_3 = self.ax.plot(
            self.x_vals_3, self.y_vals_3, linestyle="dashed")[0]

    def animate(self, data):

        self.line_1.set_xdata(data[0])
        self.line_1.set_ydata(data[1])
        self.line_2.set_xdata(data[2])
        self.line_2.set_ydata(data[3])

    def visualize(self):
        self.anim = FuncAnimation(
            self.fig, self.animate, interval=1, frames=self.data, repeat=False)
        plt.draw()
        plt.show()


"""
x1 = [[0, 0], [0, 0.1], [0, 0.2], [0, 0.3], [0, 0.4]]
y1 = [[0, -1], [0, -0.9], [0, -0.8], [0, -0.7], [0, -0.6]]
x2 = [[0, -1], [0.1, 0.2], [0.2, 0.3], [0.3, 0.4], [0.4, 0.5]]
y2 = [[-1, -2], [-0.9, -1.9], [-0.8, -1.8], [-0.7, -1.7], [-0.6, -1.6]]
x3 = [-10, 10]
y3 = [1, 1]

data = [(x1[0], y1[0], x2[0], y2[0]), (x1[1], y1[1],
                                       x2[1], y2[1]), (x1[2], y1[2], x2[2], y2[2])]

vis = Visualizer(data, 1)

vis.visualize()
"""
