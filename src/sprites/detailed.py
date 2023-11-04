""" Wall sprite """
import os

import pygame

from constants.headup import BOTTOM_UI_HEIGHT
from sprites.sprite import Sprite


class Detailed(Sprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        self.detailed = os.path.join(sprite_dir, 'detailed', sprite)
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.screen = None

    def draw(self, screen, x, y):
        self.screen = screen
        super().draw(screen, x, y)

    def handle_interact(self, element):
        """ Show details view """
        element.state.show_detailed = pygame.image.load(
            self.detailed).convert_alpha()

        x, y = self.screen.get_size()
        element.state.show_detailed = pygame.transform.smoothscale(
            element.state.show_detailed, (x, y)
        )
