""" Generic sprite """

import logging
import os

import pygame

from constants.graphics import SPRITE_SIZE
from utils.reflections import fullname


class Sprite:
    """ Generic sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        self.sprite = None
        self.sprite_file = sprite
        self.walkable = True
        self.sprite_dir = sprite_dir
        self.id = None
        self.state = None
        self.center_camera = False
        self.purge = False

        if not sprite:
            return

        file = os.path.join(sprite_dir, sprite)
        image = cache.load_image(file)

        if not image:
            logging.error('File ' + file + ' not found')
            return

        self.sprite = pygame.transform.smoothscale(image,
                                                   SPRITE_SIZE
                                                   )

    def draw(self, screen, x, y):
        """ draw sprite """
        if not self.sprite:
            return None

        pos = self.calculate_pos(x, y)

        screen.blit(self.sprite, pos)

        return pos

    def calculate_pos(self, x, y):
        """
           x and y are tile positions
           Convert to real pixel coordinates
        """
        if not self.sprite:
            return None

        width = self.sprite.get_width()
        height = self.sprite.get_height()
        return (width * x, height * y)

    def handle_interact(self, element):
        """ Handle interact"""
        return

    def change_direction(self, direction):
        """ Change sprite direction """
        return

    def to_dict(self):
        """ To dictionary """
        return {
            'sprite_class': fullname(self),
            'sprite_file': self.sprite_file,
            'walkable': int(self.walkable)
        }
