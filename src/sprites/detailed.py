""" Wall sprite """
import os

import pygame

from constants.game import SCREEN_SIZE
from constants.headup import BOTTOM_UI_HEIGHT
from sprites.sprite import Sprite


class Detailed(Sprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.detailed = os.path.join(sprite_dir, 'detailed', sprite)

    def handle_interact(self, element):
        element.state.show_detailed = pygame.image.load(
            self.detailed).convert_alpha()

        x, y = SCREEN_SIZE
        y -= BOTTOM_UI_HEIGHT
        element.state.show_detailed = pygame.transform.smoothscale(
            element.state.show_detailed, (x, y)
        )
