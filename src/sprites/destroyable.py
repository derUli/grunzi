""" Destroyable sprite """
import logging

from sprites.chainsaw import Chainsaw
from sprites.wall import Wall
import random
from utils.quality import pixel_fades_enabled
RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0


class Destroyable(Wall):
    """ Fence sprite class """

    def __init__(self, sprite_dir, cache, sprite='box.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.fadeout = False

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        if self.fadeout and not self.remove_random_pixel():
            self.stop_fade()

    def handle_interact_item(self, element):
        # Destroy if player has the chainsaw
        if not element:
            return

        if isinstance(element.state.inventory, Chainsaw) and not self.walkable:
            if element.state.inventory.attributes['fuel'] <= 0:
                return

            if pixel_fades_enabled():
                self.start_fade()
            else:
                self.purge = True

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
        self.fadeout = True
        self.walkable = True
        self.sprite = self.sprite.copy().convert_alpha()

    def stop_fade(self):
        self.fadeout = False
        self.purge = True

    def remove_random_pixel(self):
        bulk = self.sprite.get_height() * 2
        for i in range(bulk):
            w, h = self.sprite.get_size()

            rand_x = random.randint(0, w - 1)
            rand_y = random.randint(0, h - 1)

            r, g, b, a = self.sprite.get_at((rand_x, rand_y))

            if a != 0:
                self.sprite.set_at((rand_x, rand_y), (r, g, b, 0))

        for x in range(0, w):
            for y in range(0, h):
                r, g, b, a = self.sprite.get_at((x, y))
                if a > 0:
                    return True

        return False