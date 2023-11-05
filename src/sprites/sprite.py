""" Generic sprite """

import logging
import os

import pygame

import constants.graphics
from constants.graphics import SPRITE_SIZE
from utils.reflections import fullname
from constants.game import MONOTYPE_FONT, DEBUG_TILE_FONT_SIZE

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
        self.replace_with = None
        self.cache = cache
        self.debug = False

        self.debug_font_file = os.path.join(self.sprite_dir, '..', '..', 'fonts', MONOTYPE_FONT)

        if not sprite:
            return

        file = os.path.join(sprite_dir, sprite)
        image = cache.load_image(file)

        if not image:
            logging.error('File ' + file + ' not found')
            return

        self.sprite = pygame.transform.smoothscale(image, SPRITE_SIZE)

    def draw(self, screen, x, y):

        pos = self.calculate_pos(x, y)

        """ draw sprite """
        if not self.sprite:
            return None

        screen.blit(self.sprite, pos)

        return pos


    def draw_debug(self, screen, x, y, from_x, from_y):

        text_str = 'X: ' + str(from_x + x) + ' Y: ' + str(from_y + y)

        font = pygame.font.Font(
            self.debug_font_file,
            DEBUG_TILE_FONT_SIZE
        )

        text = font.render(
            text_str,
            1,
            (255, 255, 255)
        )

        pos = self.calculate_pos(x, y)
        screen.blit(text, pos)

    def calculate_pos(self, x, y):
        """
           x and y are tile positions
           Convert to real pixel coordinates
        """
        width, height = constants.graphics.SPRITE_SIZE

        return (width * x, height * y)

    def handle_interact(self, element):
        """ Handle interact"""
        return

    def handle_interact_item(self, element):
        """ Handle interact item """
        return

    def change_direction(self, direction):
        """ Change sprite direction """
        return

    def to_dict(self):
        """ To dictionary """
        data = {
            'sprite_class': fullname(self),
            'sprite_file': self.sprite_file
        }

        if self.walkable:
            data['walkable'] = int(self.walkable)

        if self.id:
            data['id'] = self.id

        return data
