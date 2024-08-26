import logging

from sprites.sprite import Sprite, AbstractAnimatedSprite
from utils.positionalsound import PositionalSound

MOVE_X = 0.5


class Ship(Sprite):
    def update(
            self,
            delta_time,
            args
    ):
        self.remove_from_sprite_lists()
        self.center_x -= MOVE_X

        if self.right < 0:
            logging.info('Removed ship from scene')
            self.remove_from_sprite_lists()


class Steam(AbstractAnimatedSprite):

    def update(
            self,
            delta_time,
            args
    ):

        self.remove_from_sprite_lists()
        self.center_x -= MOVE_X

        if self.center_x <= 3400 and not self.sound:
            audio = args.state.play_sound('ship', 'horn')
            self.sound = PositionalSound(args.player, args.player, audio, args.state)
            self.sound.update(init=True)
            self.sound.play()

        if self.sound:
            self.sound.update()

        if self.right < 0:
            self.remove_from_sprite_lists()
            logging.info('Removed steam from scene')
