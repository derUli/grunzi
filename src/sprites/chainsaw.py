""" Chainsaw sprite """
import os
import random

from constants.direction import DIRECTION_UP, DIRECTION_DOWN
from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable
from utils.audio import play_sound

SHAKE_Y_FROM = -2
SHAKE_Y_TO = 2


class Chainsaw(Takeable, InlineSprite):
    """ Chainsaw sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.shake_y = 0
        self.shake_direction = DIRECTION_DOWN

    def draw_inline(self, screen, pos):
        """ draw sprite """

        px_x, px_y = pos

        if self.shake_direction == DIRECTION_DOWN:
            self.shake_y += 1
            if self.shake_y >= SHAKE_Y_TO:
                self.shake_direction = DIRECTION_UP
        else:
            self.shake_y -= 1
            if self.shake_y <= SHAKE_Y_FROM:
                self.shake_direction = DIRECTION_DOWN

        px_y += self.shake_direction

        screen.blit(self.inline_sprite, (px_x, px_y))
        return

    def play_sound(self):
        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'chainsaw')
        )

        files = [
            'chainsaw1.ogg',
            'chainsaw2.ogg',
            'chainsaw3.ogg',
            'chainsaw4.ogg',
        ]

        play_sound(
            os.path.join(sound_dir, random.choice(files))
        )
