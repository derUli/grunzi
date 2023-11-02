""" Wall sprite """
from sprites.sprite import Sprite
import pygame
import os
import constants.game


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
        element.state.show_detailed = pygame.transform.smoothscale(
            element.state.show_detailed, (constants.game.SCREEN_SIZE))
