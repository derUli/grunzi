""" volkslehrer character sprite """
import os

import pygame

from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT
from sprites.character import Character
from sprites.killable import Killable
from sprites.weapon import Weapon
from utils.audio import play_sound

BLOOD_COLOR = (163, 8, 8)
SOUND_FADEOUT = 100
HURT_DAMAGE = 5


class Volkslehrer(Killable, Character):
    """ devilwoman sprite class """

    def __init__(self, sprite_dir, cache, sprite='volkslehrer2.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.sound_played = False


    def draw(self, screen, x, y):
        """ Draw sprite """

        super().draw(screen, x, y)

    def ai(self, level):
        if not self.sound_played:
            self.sound_played = True
            self.play_sound()
            level.get_mainchar().state.say(_('I am openly right-wing radical.'))


    def play_sound(self):
        return play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'volkslehrer',
                'volkslehrer.ogg'
            )
        )

