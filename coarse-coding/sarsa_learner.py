from importlib.metadata import distribution
import numpy as np
import time
from acrobat import Acrobat
from visualizer import Visualizer
import matplotlib.pyplot as plt
from matplotlib import animation


class Sarsa:

    def __init__(self, critic, sim_world, params):
        self.critic = critic
        self.sim_world = sim_world
        self.params = params
        self.visualize_episodes = params["visualize_episodes"]
        self.n_episodes = params["n_episodes"]
        self.max_step = params["max_step"]
        self.step_history = []
        self.filters = Acrobat.create_filters()
        self.epsilon = params['epsilon']
        self.epsilon_decay = params['epsilon_decay_rate']

    def learn(self):
        for i in range(1, self.n_episodes+1):  # Iterates through each episode at a time
            best_y = -2
            x = 0
            batch = []  # not necesarry
            j = 0  # Step counter

            game = Acrobat(self.params)

            state = game.get_state(self.filters)  # Recieve state information

            # Get all valid actions based on current state
            possible_actions = game.get_actions()
            # Let the actor choose the best action in the current state
            if i > 190:
                pass
            action = self.critic.get_action(
                state, possible_actions, self.epsilon)
            batch.append((state, action))  # Stor the state/action pair
            while not game.is_final() and j < self.max_step:  # Perfrom the step wise iteration through the episode
                # Perform the chosen action on the environment
                reward = game.update_state(action, j)  # possbly add j?
                new_state = game.get_state(self.filters)  # Get the new state
                # print("Actual state: %s" % (game.state))
                # print("-------------------------------")

                # Get all valid actions based on new state
                possible_actions = game.get_actions()
                # Let the actor choose the best action
                new_action = self.critic.get_action(
                    new_state, possible_actions, self.epsilon)

                # for s, a in batch:  # Iterate through each state/action pair in current episode to update value/eligibility
                target = self.critic.calculate_target(
                    reward, new_state, new_action)
                self.critic.train(state, action, target)

                state = new_state
                action = new_action

                # Append current state/action pair to batch
                batch.append((new_state, new_action))
                j += 1

                if game.y_tip > best_y:
                    best_y = game.y_tip
                    x = game.x_tip

            if game.is_final():
                vis = Visualizer(game.all_states_in_episode, 1)
                vis.visualize()
                writergif = animation.PillowWriter(fps=30)

                vis.anim.save(
                    f"/Users/akselostmoe/Skole/4. klasse vår 2022/AI prog/exercises/exercise 3/Coarse-Coding/episode_{i}_steps_{j}.gif", writer=writergif)
            print("------------ EPISODE (%s) --- STEPS (%s) --------------" % (i, j))
            dist = game.num_distribution
            # plt.bar(*zip(*dist.items()))
            # plt.show()
            # vis = Visualizer(game.all_states_in_episode, 1)
            # vis.visualize()
            # game.num_step(j)
            self.step_history.append(j)
            print("best (x,y): (%s, %s)" % (x, best_y))
            # self.epsilon -= self.epsilon_decay
            if i in self.visualize_episodes:
                game.visualize_current_episode(self.delay)
        if -1 in self.visualize_episodes:
            self.sim_world.visualize_best_episode()
