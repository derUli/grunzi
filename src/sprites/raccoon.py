""" Racoon character """
import os

import constants.graphics
import constants.direction
import sprites.character
import utils.audio


class Raccoon(sprites.character.Character):
    """ Raccon character class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'raccoon.png')
        self.center_camera = False

    def handle_interact(self, element):
        """ Play sound on interaction """
        if element.direction == constants.direction.DIRECTION_LEFT:
            self.change_direction(constants.direction.DIRECTION_RIGHT)
        elif element.direction == constants.direction.DIRECTION_RIGHT:
            self.change_direction(constants.direction.DIRECTION_LEFT)

        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'kiss.ogg'))
        utils.audio.play_sound(sound_dir)
