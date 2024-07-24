from sprites.sprite import AbstractAnimatedSprite
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_SOUND


class Fire(AbstractAnimatedSprite):

    def update(
            self,
            delta_time,
            args
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

