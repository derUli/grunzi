""" Generic sprite """

import logging
import os

import pygame

import constants.graphics
import utils.quality
from constants.game import MONOTYPE_FONT, DEBUG_TILE_FONT_SIZE
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

        self.mov_offset_x = 0
        self.mov_offset_y = 0

        self.purge = False
        self.replace_with = None
        self.cache = cache
        self.debug = False
        self.debug_font_file = os.path.join(self.sprite_dir, '..', '..', 'fonts', MONOTYPE_FONT)
        self.debug_font = None
        self.attributes = {}
        self.player_state = None

        if not sprite:
            return

        file = os.path.join(sprite_dir, sprite)
        self.sprite = cache.load_image(file, SPRITE_SIZE)

        if not self.sprite:
            logging.error('File ' + file + ' not found')
            return

    def init_state(self):
        self.state = None

    def draw(self, screen, x, y):

        pos = self.calculate_pos(x, y)

        """ draw sprite """
        if not self.sprite:
            return None

        return screen.blit(self.sprite, pos)

    def draw_debug(self, screen, x, y, from_x, from_y):

        text_str = 'X: ' + str(from_x + x) + ' Y: ' + str(from_y + y)

        if not self.debug_font:
            self.debug_font = pygame.font.Font(
                self.debug_font_file,
                DEBUG_TILE_FONT_SIZE
            )

        text = self.debug_font.render(
            text_str,
            utils.quality.font_antialiasing_enabled(),
            (255, 255, 255)
        )

        pos_x, pos_y = self.calculate_pos(x, y)

        pos_y -= DEBUG_TILE_FONT_SIZE

        if pos_y < 0:
            pos_y = 0
        screen.blit(text, (pos_x, pos_y))

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
            'sprite_file': self.sprite_file,
        }

        if self.walkable:
            data['walkable'] = int(self.walkable)

        if self.id:
            data['id'] = self.id

        if self.attributes:
            data['attributes'] = self.attributes

        return data

    def ai(self, level):
        return
