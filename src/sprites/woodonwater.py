""" Wall sprite """
from sprites.sprite import Sprite


class WoodOnWater(Sprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='wood.jpg'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.level = None
        self.can_swim = False

    def handle_interact(self, element):
        pass
