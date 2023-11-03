""" Wall sprite """
import os

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
            os.path.join(sprite_dir, '..', '..', 'sounds', 'door_open.ogg')
        )

        self.door_closed_sound = os.path.abspath(
            os.path.join(sprite_dir, '..', '..', 'sounds', 'door_closed.ogg')
        )

    def handle_interact(self, element):
        """ Set walkable on interact """

        if not element:
            return

        # Todo: Check for Key
        # Play sound on unlock
        if not self.walkable and not element.state.inventory:
            play_sound(self.door_closed_sound)
            return

        self.open_door(element)

    def open_door(self, element=None):
        play_sound(self.door_open_sound)

        self.walkable = True
        element.state.inventory = None
