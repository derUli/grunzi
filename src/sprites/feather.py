""" Wall sprite """

from sprites.takeable import Takeable


class Feather(Takeable):
    """ Takeable sprite class """

    def __init__(self, sprite_dir, cache, sprite='feather.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
