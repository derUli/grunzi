""" Wall sprite """
from sprites.wall import Wall
from utils.audio import play_sound
import os


class Takeable(Wall):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='key1.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        # For unlocking just set this on true
        self.walkable = True

    def handle_interact(self, element):
        """ Set walkable on interact """

        element.state.inventory = self

        # TODO Remove item from world
