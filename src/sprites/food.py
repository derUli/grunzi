""" Apple sprite class """
import logging
import os

import sprites.sprite
from utils.audio import play_sound


class Food(sprites.sprite.Sprite):
    """ Apple sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.nutritional_value = 0

    def handle_interact(self, element):
        """ Food increases health """

        if self.nutritional_value == 0:
            logging.error('nutritional_value not set')
            return

        if element and element.state and element.state.health < 100:
            element.state.partial_heal(30)
            self.purge = True
            self.walkable = True

            sound = os.path.abspath(
                os.path.join(
                    self.sprite_dir,
                    '..',
                    '..',
                    'sounds',
                    'pig',
                    'smacks.ogg')
            )

            play_sound(sound)
