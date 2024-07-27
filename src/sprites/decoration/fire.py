import arcade

from sprites.sprite import AbstractAnimatedSprite
from state.argscontainer import ArgsContainer
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_SOUND


class Fire(AbstractAnimatedSprite):

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ):
        super().update(delta_time, args)
        if not hasattr(self, 'fx'):
            audio = args.state.play_sound('fire', loop=True)
            self.fx = PositionalSound(
                args.player,
                self,
                audio,
                args.state,
                volume_source=VOLUME_SOURCE_SOUND
            )
            self.fx.update(init=True)
            return

        self.fx.update()

        # Hurt player
        if arcade.check_for_collision(self, args.player):
            args.player.hurt(2)
