""" devilwoman character sprite """
import os

import pygame

from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT
from sprites.character import Character
from sprites.killable import Killable
from sprites.weapon import Weapon
from utils.audio import play_sound

BLOOD_COLOR = (163, 8, 8)
SOUND_FADEOUT = 100
HURT_DAMAGE = 5


class DevilWoman(Killable, Character):
    """ devilwoman sprite class """

    def __init__(self, sprite_dir, cache, sprite='devilwoman.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction
        self.sounds = {}
        self.bulk_size = 5

    def draw(self, screen, x, y):
        """ Draw sprite """

        sprite = self.sprite.copy()

        flip_x = False
        flip_y = False

        if self.image_direction == DIRECTION_LEFT:
            flip_x = True
        sprite = pygame.transform.flip(sprite, flip_x, flip_y)

        pos = self.calculate_pos(x, y)

        return sprite, pos

    def ai(self, level):
        mainchar_z, mainchar_y, mainchar_x = level.search_mainchar()
        pos = level.search_sprite(self)

        if not pos:
            return

        devilwoman_z, devilwoman_y, devilwoman_x = pos

        if mainchar_x > devilwoman_x:
            self.change_direction(DIRECTION_RIGHT)
        else:
            self.change_direction(DIRECTION_LEFT)

    def handle_interact(self, element):
        if self.killed():
            return

        element.state.say(_('Heavy Metal, dude!'))

        if 'meddl' in self.sounds and self.sounds['meddl'].get_busy():
            return

        self.sounds['meddl'] = self.play_sound()

    def handle_interact_item(self, element):
        if self.killed():
            return

        if isinstance(element.state.inventory, Weapon):
            self.kill()

            if 'scream' in self.sounds and self.sounds['scream'].get_busy():
                return

            if 'meddl' in self.sounds and self.sounds['meddl'].get_busy():
                self.sounds['meddl'].stop()

            self.sounds['scream'] = self.scream()

    def play_sound(self):
        return play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'devilwoman',
                'devilwoman.ogg'
            )
        )

    def scream(self):
        return play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'devilwoman',
                'scream.ogg'
            )
        )
