""" Wall sprite """

from sprites.takeable import Takeable
from sprites.inlinesprite import InlineSprite


class Coin(Takeable, InlineSprite):
    """ Takeable sprite class """

    def __init__(self, sprite_dir, cache, sprite='coin.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
