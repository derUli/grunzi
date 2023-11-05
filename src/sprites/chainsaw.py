""" Chainsaw sprite """
import os
import random

from sprites.takeable import Takeable
from sprites.inlinesprite import InlineSprite
from utils.audio import play_sound


class Chainsaw(Takeable, InlineSprite):
    """ Chainsaw sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

    def play_sound(self):
        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'chainsaw')
        )

        files = [
            'chainsaw1.ogg',
            'chainsaw2.ogg',
            'chainsaw3.ogg',
            'chainsaw4.ogg',
        ]

        play_sound(
            os.path.join(sound_dir, random.choice(files))
        )
