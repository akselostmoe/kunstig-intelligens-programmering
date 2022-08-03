from critic import Critic
from sarsa_learner import Sarsa
from config import create_config
from acrobat import Acrobat
import cProfile
import time


def main():

    params = create_config()
    
    critic = Critic(params)
    sim_world = Acrobat(params)

    learner = Sarsa(critic, sim_world, params)
    learner.learn()


if __name__ == '__main__':
    #cProfile.run('main()', sort='cumtime')
    main()
