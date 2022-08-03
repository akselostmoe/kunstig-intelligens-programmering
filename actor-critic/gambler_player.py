
class GamblerPlayer:

    def __init__(self, gambler_world):
        self.gambler_world = gambler_world

    def do_action(self, bet):
        self.gambler_world.update(bet)
        if self.gambler_world.units == 100:
            return 100
        elif self.gambler_world.units == 0:
            return -100
        else:
            return 0
