""" Apple sprite class """
import os

import sprites.sprite
from utils.audio import play_sound


class Apple(sprites.sprite.Sprite):
    """ Apple sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'apple.png')

    def handle_interact(self, element):
        """ Apple increases health """
        if element and element.state and element.state.health < 100:
            element.state.partial_heal(30)
            self.purge = True
            self.walkable = True

            sound = os.path.abspath(
                os.path.join(self.sprite_dir, '..', '..', 'sounds', 'pig', 'smacks.ogg')
            )

            play_sound(sound)
