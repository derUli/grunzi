from sprites.sprite import Sprite
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_ATMO

MOVE_SPEED = 5


class River(Sprite):
    def update(
            self,
            delta_time,
            args
    ):
        w, h = args.map_size
        if self.alpha > 200:
            self.alpha = 200

        self.center_x -= MOVE_SPEED

        if self.right <= 0:
            self.right = w - abs(self.right)


class RiverSound(Sprite):
    def update(self, delta_time, args):
        if not hasattr(self, 'sound'):
            audio = args.state.play_sound('atmos', 'river', loop=True)
            self.sound = PositionalSound(
                args.player,
                self,
                audio,
                args.state,
                volume_source=VOLUME_SOURCE_ATMO
            )

        from constants.layers import LAYER_RIVER

        # TODO: Fade out volume based on water level
        if not any(args.scene[LAYER_RIVER]):
            self.sound.pause()
            return

        self.sound.update()
