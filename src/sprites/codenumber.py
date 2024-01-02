""" Wall sprite """
import os

import pygame

from constants.graphics import SPRITE_SIZE
from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable
from utils.quality import font_antialiasing_enabled

W, H = SPRITE_SIZE
TEXT_COLOR = (0, 0, 0)
FONT_SIZE = H
TEXT_FONT = 'adrip1.ttf'
OFFSET_X = 0
OFFSET_Y = 7


class CodeNumber(Takeable, InlineSprite):
    """ Takeable sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.sprite = pygame.surface.Surface(SPRITE_SIZE, pygame.SRCALPHA)
        self.drawn_text = None

        self.attributes = {
            'digit': 1
        }

        self.font = pygame.font.Font(
            os.path.join(self.sprite_dir, '..', '..', 'fonts', TEXT_FONT),
            FONT_SIZE
        )

    def handle_interact(self, element):
        if 'locked' in self.attributes and self.attributes['locked']:
            return

        super().handle_interact(element)

    def draw(self, screen, x, y):
        """ Draw text """
        if not self.drawn_text:
            self.drawn_text = self.font.render(
                str(self.attributes['digit']),
                font_antialiasing_enabled(),
                TEXT_COLOR
            )

            text_x = W / 2 - self.drawn_text.get_width() / 2 + OFFSET_X
            text_y = H / 2 - self.drawn_text.get_height() / 2 + OFFSET_Y

            self.sprite.blit(self.drawn_text, (text_x, text_y))

        pos = self.calculate_pos(x, y)

        screen.blit(self.sprite, pos)
