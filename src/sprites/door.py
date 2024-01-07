""" Wall sprite """
import os

from sprites.key import Key
from sprites.wall import Wall
from utils.audio import play_sound


class Door(Wall):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='door.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        # For unlocking just set this on true
        self.walkable = False

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

        # Play sound on unlock
        if not self.walkable:
            play_sound(self.door_closed_sound)
            element.state.say(_('The door is closed. I need a key.'))
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
            self.walkable = True

            element.state.say(_('The door is now open.'))
