""" Destroyable sprite """
import logging
import pygame
from sprites.chainsaw import Chainsaw
from sprites.wall import Wall
import random
from utils.quality import pixel_fades_enabled
from threading import Thread

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0


class Destroyable(Wall):
    """ Fence sprite class """

    def __init__(self, sprite_dir, cache, sprite='box.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.persistent_pixels = 0
        self.fadeout = False

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

    def handle_interact_item(self, element):
        # Destroy if player has the chainsaw
        if not element:
            return

        if isinstance(element.state.inventory, Chainsaw) and not self.walkable and not self.fadeout:
            if element.state.inventory.attributes['fuel'] <= 0:
                return

            if pixel_fades_enabled():
                if not self.fadeout:
                    self.start_fade()
            else:
                self.purge = True
                self.walkable = True

                logging.debug('Destroyable sprite destroyed with chainsaw')

            element.state.inventory.play_sound()

            # Rumble on gamepad if we have one
            if element.state.gamepad:
                element.state.gamepad.joystick.rumble(
                    RUMBLE_CHAINSAW_LOW_FREQUENCY,
                    RUMBLE_CHAINSAW_HIGH_FREQUENCY,
                    RUMBLE_CHAINSAW_DURATION
                )

    def start_fade(self):
        self.sprite = self.sprite.copy().convert_alpha()
        self.persistent_pixels = self.count_persistent_pixels()
        self.fadeout = True

        thread = Thread(target=self.remove_pixels)
        thread.start()


    def stop_fade(self, purge = False):
        self.fadeout = False
        self.purge = purge
        logging.debug('Destroyable sprite destroyed with chainsaw')

    def remove_pixels(self):
        bulk = 5
        while self.fadeout:
            pygame.time.delay(1)
            for i in range(bulk):
                self.remove_random_pixel()

    def remove_random_pixel(self):
        w, h = self.sprite.get_size()

        if self.persistent_pixels <= 0:
            self.stop_fade(purge=True)
            return

        r,g,b,a = 0, 0, 0, 0
        rand_x = 0
        rand_y = 0

        while a == 0:
            rand_x = random.randint(0, w - 1)
            rand_y = random.randint(0, h - 1)

            r, g, b, a = self.sprite.get_at((rand_x, rand_y))

        self.sprite.set_at((rand_x, rand_y), (r, g, b, 0))
        self.persistent_pixels -= 1


    def count_persistent_pixels(self):
        persistent = 0
        w, h = self.sprite.get_size()
        for x in range(0, w):
            for y in range(0, h):
                r, g, b, a = self.sprite.get_at((x, y))
                if a > 0:
                    persistent += 1

        return persistent
