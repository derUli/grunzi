""" Player sprite class """
from sprites.sprite import AnimatedSprite
from state.argscontainer import ArgsContainer
from utils.positionalsound import PositionalSound


class Crystal(AnimatedSprite):
    def setup(self, args):
        audio = args.state.play_sound('boss', 'crystal', loop=True)
        self.sound = PositionalSound(args.player, self, audio, args.state)
        self.sound.play()

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ) -> None:
        super().update(delta_time, args)
        self.sound.update()
