from pole_balancing_world import PoleBalancingWorld


class PoleBalancingPlayer:

    def __init__(self, pole_balancing_world):
        self.pole_balancing_world = pole_balancing_world
        self.alive_reward = 3
        self.loss_reward = -100

    def do_action(self, B):
        self.pole_balancing_world.update_per_timestep(self.B_to_F(B))
        if self.pole_balancing_world.game_over():
            reward = self.loss_reward
        else:
            reward = self.alive_reward
        return reward

    # helper to convert binary input to force (F)
    def B_to_F(self, B):
        if B == "0":
            return -self.pole_balancing_world.F
        else:
            return self.pole_balancing_world.F
