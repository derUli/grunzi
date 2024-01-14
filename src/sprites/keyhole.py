""" Keyhole sprite """
import os

from sprites.fadeable import Fadeable
from sprites.key import Key
from utils.audio import play_sound


class Keyhole(Fadeable):
    """ Keyhole sprite class """

    def __init__(self, sprite_dir, cache, sprite='keyhole.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        # For unlocking just set this on true
        self.walkable = False
        self.id = 'door-2'

        self.door_open_sound = os.path.abspath(
            os.path.join(
                sprite_dir,
                '..',
                '..',
                'sounds',
                'door',
                'door_open.ogg')
        )

        self.door_closed_sound = os.path.abspath(
            os.path.join(
                sprite_dir,
                '..',
                '..',
                'sounds',
                'door',
                'door_closed.ogg')
        )

    def handle_interact(self, element):
        """ Handle interaction witohut item """
        # Play sound on unlock
        if not self.walkable:
            play_sound(self.door_closed_sound)

            element.state.say(_('There is a keyhole in the wall.'))
            return

        play_sound(self.door_open_sound)

    def handle_interact_item(self, element):
        """ Set walkable on interact """

        if not element:
            return

        item = element.state.inventory

        number = self.id.split('-')[1]
        expected_id = "key-" + number

        if isinstance(
                item, Key) and not self.walkable and item.id == expected_id:
            self.open_door()
            return

    def open_door(self):
        self.start_fade()
