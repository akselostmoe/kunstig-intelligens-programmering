
# The actor-critic algorithm based on the pseudo-code in actor-critic.pdf
from cmath import inf
from actor import Actor
from critic import Critic
from pole_balancing_player import PoleBalancingPlayer
from pole_balancing_world import PoleBalancingWorld
from towers_of_hanoi_player import TowerOfHanoiPlayer
from towers_of_hanoi_world import TowersOfHanoiWorld
from gambler_world import GamblerWorld
from gambler_player import GamblerPlayer
from config import create_config
import matplotlib.pyplot as plt
import cProfile


def main():
    dictionary = create_config()
    actor_critic = AC_algorithm(dictionary)
    actor_critic.algorithm()


class AC_algorithm:

    def __init__(self, config_dict):

        self.config_dict = config_dict

        # first setting all pivotal parameters:
        self.actor_decay_rate = config_dict["actor_decay_rate"]
        self.critic_decay_rate = config_dict["critic_decay_rate"]
        self.epsilon = config_dict["epsilon"]
        self.actor_learning_rate = config_dict["actor_learning_rate"]
        self.critic_learning_rate = config_dict["critic_learning_rate"]
        self.actor_discount_factor = config_dict["actor_discount_factor"]
        self.critic_discount_factor = config_dict["critic_discount_factor"]
        self.episodes = config_dict["episodes"]
        self.max_timesteps = config_dict["max_timesteps"]
        self.epsilon_decrease = config_dict["epsilon_decrease"]
        self.ann_binary = config_dict["ann_binary"]
        self.task = config_dict["task"]
        self.episodes_to_visualize = config_dict["episodes_to_visualize"]

        self.timesteps_reached_list = []
        self.episode_performance_list = []
        self.best_world = 0

        # task specific parameters:
        if self.task == 1:
            self.L = config_dict["L"]
            self.M_p = config_dict["M_p"]
            self.G = config_dict["G"]
            self.tau = config_dict["tau"]
            self.input_dims = 4
        elif self.task == 2:
            self.pegs = config_dict["pegs"]
            self.discs = config_dict["discs"]
            self.input_dims = self.pegs * self.discs
        else:
            self.win_probability = config_dict["win_probability"]
            self.input_dims = 1

        # critic (table or ANN) specific parameters:
        self.layers = config_dict["layers"]

        self.actor = Actor(self.actor_decay_rate, self.epsilon, self.actor_learning_rate,
                           self.actor_discount_factor)
        self.critic = Critic(
            self.critic_decay_rate, self.critic_learning_rate, self.critic_discount_factor, self.ann_binary, self.input_dims, self.layers)

    def algorithm(self):
        for episode in range(self.episodes):
            print("XXXXXXXXXXXXXXXXXXX")
            print("Episode: " + str(episode))
            # resetting critic and actor and creating world and player
            self.critic.episode_reset()
            self.actor.episode_reset(self.epsilon_decrease)
            # making the world and player based on task
            if self.task == 1:
                world = PoleBalancingWorld(self.L, self.M_p, self.G, self.tau)
                player = PoleBalancingPlayer(world)
            elif self.task == 2:
                world = TowersOfHanoiWorld(self.pegs, self.discs)
                player = TowerOfHanoiPlayer(world)
            else:
                world = GamblerWorld(self.win_probability)
                player = GamblerPlayer(world)
            # initial state and action
            string_state = world.convert_state_to_string()
            list_state = world.convert_state_to_list()
            action = self.actor.next_action(string_state, world)

            # lists of states for each timestep in an episode, resets each episode
            episode_list_state_history = [list_state]
            timestep_counter = 0
            for timestep in range(self.max_timesteps):
                # doing action, receiving reward and moving the world to a new state
                reward = player.do_action(action)
                # state_marked and action_marked are s' and a' from the pesudo-code
                string_state_marked = world.convert_state_to_string()
                list_state_marked = world.convert_state_to_list()
                episode_list_state_history.append(list_state_marked)
                action_marked = self.actor.next_action(
                    string_state_marked, world)
                self.actor.eligibility_set(string_state, action)
                self.critic.eligibility_set(string_state)
                td_error = self.critic.calculate_td_error(
                    string_state, string_state_marked, reward)
                target = self.critic.get_target_value(
                    reward, list_state_marked)
                self.critic.update_vals(td_error, target, list_state, timestep)
                self.actor.update_vals(td_error)
                list_state = list_state_marked
                string_state = string_state_marked
                action = action_marked
                timestep_counter += 1
                if world.game_over():
                    print("Timesteps: " + str(timestep + 1) +
                          "/" + str(self.max_timesteps))
                    break
            self.timesteps_reached_list.append(timestep_counter)
            if timestep_counter == self.max_timesteps:
                print("Timesteps: " + str(timestep + 1) +
                      "/" + str(self.max_timesteps))
                self.best_world = world
            if ((episode + 1) in self.episodes_to_visualize):
                world.visualize(episode_list_state_history,
                                self.timesteps_reached_list, self.best_world, self.actor)

        episode_list_state_history = []

        # make visualization at the end
        world.visualize(episode_list_state_history,
                        self.timesteps_reached_list, self.best_world, self.actor)


if __name__ == '__main__':
    # cProfile.run('main()', sort='cumtime')
    main()
