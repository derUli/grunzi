""" Burger sprite class """
import os

import sprites.sprite
from utils.audio import play_sound


class Burger(sprites.sprite.Sprite):
    """ Burger sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'burger.png')

    def handle_interact(self, element):
        """ Burger increases health """
        if element and element.state and element.state.health < 100:
            element.state.partial_heal(60)
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
