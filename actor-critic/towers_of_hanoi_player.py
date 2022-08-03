
class TowerOfHanoiPlayer:
    def __init__(self, hanoi_world):
        self.hanoi_world = hanoi_world
        self.continue_reward = -0.1
        self.win_reward = 100

    def do_action(self, action):
        self.hanoi_world.update(action)
        if self.hanoi_world.game_over():
            reward = self.win_reward
        else:
            reward = self.continue_reward
        return reward
