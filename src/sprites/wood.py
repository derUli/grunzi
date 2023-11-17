""" Wall sprite """
from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable


class Wood(Takeable, InlineSprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='wood.jpg'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)


