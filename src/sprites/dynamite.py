""" Wall sprite """
from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable
from threading import Thread
from stopwatch import Stopwatch
from utils.audio import play_sound
import os

COUNT_TO = 5
class Dynamite(Takeable):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='dynamite.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.clock = Stopwatch()
        self.clock.stop()
        self.last_second = 0

    def ai(self, level):

        if not self.clock.running:
            return

        second = int(self.clock.duration)

        # TODO: Add visual countdown to dynamyte image
        if second > self.last_second:
            self.last_second = second
            self.play_countdown_sound()
        
        # TODO: If countdown expired explode
        if second >= COUNT_TO:
            self.clock.stop()
            self.play_explosion_sound()


    def play_countdown_sound(self):
        play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'common',
                'countdown.ogg'
            )
        )

    def play_explosion_sound(self):
        play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'common',
                'explosion.ogg'
            )
        )