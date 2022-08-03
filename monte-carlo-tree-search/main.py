import cProfile
from pstats import Stats

from config import create_config
from reinforcementlearner import RL_algorithm
from topp import Topp


def main():
    dictionary = create_config()
    if dictionary["run_mcts"]:
        mcts = RL_algorithm(dictionary)
        mcts.algorithm()
    if dictionary["run_topp"]:
        topp = Topp(dictionary)
        topp.tournament()


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()
    main()
    pr.disable()
    stats = Stats(pr)
    stats.sort_stats("tottime").print_stats(10)

    # main()
