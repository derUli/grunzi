""" Wall sprite """
from sprites.takeable import Takeable
from sprites.inlinesprite import InlineSprite


class Key(Takeable, InlineSprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='key1.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
