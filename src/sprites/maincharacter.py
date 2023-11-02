""" Main character sprite """

import pygame
from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT
from sprites.character import Character
import constants.game

class MainCharacter(Character):
    """ Main character sprite class """

    def __init__(self, sprite_dir, cache, sprite='pig.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        
        self.center_camera = True

        # One tile by second
        self.walk_speed = 0.3
        self.sprint_speed = self.walk_speed * 0.2
        self.last_movement = 0
        self.id = constants.game.MAIN_CHARACTER_ID
