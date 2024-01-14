""" Destroyable sprite """
import logging

from sprites.chainsaw import Chainsaw
from sprites.fadeable import Fadeable
from sprites.wall import Wall
from utils.quality import pixel_fades_enabled

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0


class Destroyable(Fadeable, Wall):
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

        if self.destroyed():
            return

        if isinstance(element.state.inventory, Chainsaw):
            if element.state.inventory.attributes['fuel'] <= 0:
                return

            self.start_fade()

            logging.debug('Destroyable sprite destroyed with chainsaw')

            element.state.inventory.play_sound()

            # Rumble on gamepad if we have one
            if element.state.gamepad:
                element.state.gamepad.joystick.rumble(
                    RUMBLE_CHAINSAW_LOW_FREQUENCY,
                    RUMBLE_CHAINSAW_HIGH_FREQUENCY,
                    RUMBLE_CHAINSAW_DURATION
                )

    def destroyed(self):
        return self.walkable or self.fadeout or self.purge
