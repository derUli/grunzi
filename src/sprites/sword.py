""" Chainsaw sprite """
import os
import random

from constants.direction import DIRECTION_UP, DIRECTION_DOWN
from sprites.fuel import Fuel
from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable
from sprites.weapon import Weapon

from utils.audio import play_sound

SHAKE_Y_FROM = -2
SHAKE_Y_TO = 2


class Sword(Takeable, InlineSprite, Weapon):
    """ Chainsaw sprite class """

    def __init__(self, sprite_dir, cache, sprite='sword.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
       
