""" Microwave which can be destroyed with dynamite """
from sprites.sprite import Sprite


class Microwave(Sprite):
    """ Microwave sprite class """

    def __init__(self, sprite_dir, cache, sprite='microwave.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
