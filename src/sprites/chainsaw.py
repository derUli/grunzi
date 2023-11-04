""" Wall sprite """

from sprites.takeable import Takeable


class Chainsaw(Takeable):
    """ Takeable sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
