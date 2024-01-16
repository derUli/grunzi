""" Frog character sprite """
import os
import random
import time

from constants.graphics import SPRITE_SIZE
from sprites.character import Character
from utils.audio import play_sound

FROG_SPEED = 0.05

CROP_MODIFIER_MIN = 0.6
CROP_MODIFIER_MAX = 1.0


class Frog(Character):
    """ Frog sprite class """

    def __init__(self, sprite_dir, cache, sprite='frog.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.next_quack = None
        self.sound = None
        self.h = None
        self.target_h = None
        self.next_target_h_update = 0
        self.h_min = None
        self.h_max = None

    def play_sound(self):
        if self.sound and self.sound.get_busy():
            return

        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'frog')
        )

        files = [
            'frog1.ogg',
            'frog2.ogg',
            'frog3.ogg',
            'frog4.ogg',
        ]

        file = os.path.join(sound_dir, random.choice(files))

        self.sound = play_sound(file)

    def draw(self, screen, x, y):
        """ draw sprite """
        x, y = self.calculate_pos(x, y)

        if not self.sprite:
            return None

        ow, oh = SPRITE_SIZE

        if not self.h:
            self.h = self.sprite.get_height()
            self.h_min = self.sprite.get_height() * CROP_MODIFIER_MIN
            self.h_max = self.sprite.get_height() * CROP_MODIFIER_MAX

        if time.time() > self.next_target_h_update:
            self.next_target_h_update = time.time() + random.randint(2, 5)
            self.target_h = random.randint(int(oh * CROP_MODIFIER_MIN), oh * CROP_MODIFIER_MAX)

        rect = (0, 0, ow, self.h)

        if self.target_h > self.h:
            self.h += FROG_SPEED
        elif self.target_h < round(self.h):
            self.h -= FROG_SPEED

        if self.h >= self.h_max:
            self.h = self.h_max
        elif self.h <= self.h_min:
            self.h = self.h_min

        return screen.blit(self.sprite, (x, y), rect)

    def ai(self, level):
        next_quack = time.time() + random.randint(0, 10)
        if not self.next_quack:
            self.next_quack = next_quack
            return

        sound_busy = self.sound and self.sound.get_busy()
        if time.time() > self.next_quack and not sound_busy:
            self.next_quack = next_quack
            self.play_sound()
