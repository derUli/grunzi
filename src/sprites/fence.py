""" Fence sprite """
import logging

from sprites.chainsaw import Chainsaw
from sprites.destroyable import Destroyable

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0


class Fence(Destroyable):
    """ Fence sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)