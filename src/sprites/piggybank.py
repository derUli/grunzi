""" Piggybank sprite """
import logging
import os
from sprites.hammer import Hammer
from sprites.wall import Wall
from utils.audio import play_sound

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0

class PiggyBank(Wall):
    """ Piggybank sprite class """

    def __init__(self, sprite_dir, cache, sprite='piggy_bank.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

    def handle_interact_item(self, element):
        # Destroy if player has a hammer
        if not element:
            return

        if isinstance(element.state.inventory, Hammer) and not self.walkable:
            logging.debug('Piggy bank destroyed with hammer')

            self.walkable = True
            self.purge = True
            self.play_sound()

            # Rumble on gamepad if we have one
            if element.state.gamepad:
                element.state.gamepad.joystick.rumble(
                    RUMBLE_CHAINSAW_LOW_FREQUENCY,
                    RUMBLE_CHAINSAW_HIGH_FREQUENCY,
                    RUMBLE_CHAINSAW_DURATION
                )

    def play_sound(self):
        play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'hammer',
                'destroy-piggybank.ogg'
            )
        )
