import constants.graphics
import constants.direction
from constants.direction import *
import components.sprites.character
import pygame
import utils.audio
import os


class Raccoon(components.sprites.character.Character):

    def __init__(self, sprite_dir, cache, sprite=None):
        super().__init__(sprite_dir, cache, 'raccoon.png')
        self.center_camera = False

    def handle_interact(self, object):
        if object.direction == constants.direction.DIRECTION_LEFT:
            self.change_direction(constants.direction.DIRECTION_RIGHT)
        elif object.direction == constants.direction.DIRECTION_RIGHT:
            self.change_direction(constants.direction.DIRECTION_LEFT)

        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'kiss.ogg'))
        utils.audio.play_sound(sound_dir)
