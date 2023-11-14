""" Destroyable sprite """
import logging

from sprites.chainsaw import Chainsaw
from sprites.wall import Wall

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0


class Destroyable(Wall):
    """ Fence sprite class """

    def __init__(self, sprite_dir, cache, sprite='box.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

    def handle_interact_item(self, element):
        # Destroy if player has the chainsaw
        if not element:
            return

        if isinstance(element.state.inventory, Chainsaw) and not self.walkable:
            if element.state.inventory.attributes['fuel'] <= 0:
                return

            self.walkable = True
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
