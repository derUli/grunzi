""" Destroyable sprite """
import random
from threading import Thread

import pygame

from sprites.sprite import Sprite
from utils.quality import pixel_fades_enabled

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0


class Killable(Sprite):
    """ Fence sprite class """

    def __init__(self, sprite_dir, cache, sprite='box.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.persistent_pixels = 0
        self.fadeout = False

    def kill(self):
        if pixel_fades_enabled():
            if not self.fadeout:
                self.start_fade()
        else:
            self.walkable = True
            self.purge = True

    def start_fade(self):
        self.fadeout = True
        self.sprite = self.sprite.copy().convert_alpha()
        self.persistent_pixels = self.count_persistent_pixels()

        thread = Thread(target=self.remove_pixels)
        thread.start()

    def stop_fade(self):
        self.fadeout = False
        self.purge = True

    def remove_pixels(self):
        bulk = 10
        while self.fadeout:
            pygame.time.wait(1)
            for i in range(bulk):
                self.remove_random_pixel()

    def remove_random_pixel(self):
        w, h = self.sprite.get_size()

        if self.persistent_pixels <= 0:
            self.stop_fade()
            return

        r, g, b, a = 0, 0, 0, 0
        rand_x = 0
        rand_y = 0

        while a == 0:
            rand_x = random.randint(0, w - 1)
            rand_y = random.randint(0, h - 1)

            r, g, b, a = self.sprite.get_at((rand_x, rand_y))

        self.sprite.set_at((rand_x, rand_y), (255, 0, 0, a))
        self.persistent_pixels -= 1

    def count_persistent_pixels(self):
        persistent = 0
        w, h = self.sprite.get_size()
        for x in range(0, w):
            for y in range(0, h):
                r, g, b, a = self.sprite.get_at((x, y))
                if r != 255 and g != 0 and b != 0:
                    persistent += 1

        return persistent

    def killed(self):
        return self.walkable or self.fadeout or self.purge

    def rumble(self, gamepad):
        # Rumble on gamepad if we have one
        if gamepad:
            gamepad.joystick.rumble(
                RUMBLE_CHAINSAW_LOW_FREQUENCY,
                RUMBLE_CHAINSAW_HIGH_FREQUENCY,
                RUMBLE_CHAINSAW_DURATION
            )
