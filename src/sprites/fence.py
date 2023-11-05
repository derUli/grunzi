""" Fence sprite """
import logging
import os
import random

from sprites.chainsaw import Chainsaw
from sprites.wall import Wall
from utils.audio import play_sound

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0


class Fence(Wall):
    """ Fence sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

    def handle_interact(self, element):
        logging.debug('interact')
        # Destroy if player has the chainsaw
        if not element:
            return

        logging.debug('inventory ' + str(element.state.inventory))

        if isinstance(element.state.inventory, Chainsaw) and not self.walkable:
            self.walkable = True
            self.purge = True

            sound_dir = os.path.abspath(
                os.path.join(self.sprite_dir, '..', '..', 'sounds', 'chainsaw')
            )

            logging.debug('Fence sprite destroyed with chainsaw')

            files = [
                'chainsaw1.ogg',
                'chainsaw2.ogg',
                'chainsaw3.ogg',
                'chainsaw4.ogg',
            ]

            play_sound(
                os.path.join(sound_dir, random.choice(files))
            )

            # Rumble on gamepad if we have one
            if element.state.gamepad:
                element.state.gamepad.joystick.rumble(
                    RUMBLE_CHAINSAW_LOW_FREQUENCY,
                    RUMBLE_CHAINSAW_HIGH_FREQUENCY,
                    RUMBLE_CHAINSAW_DURATION
                )
