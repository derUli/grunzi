""" Hammer sprite """

from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable

class Hammer(Takeable, InlineSprite):
    """ Hammer sprite class """

    def __init__(self, sprite_dir, cache, sprite='hammer.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

