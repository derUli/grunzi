""" Wall sprite """
from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable
from threading import Thread
from stopwatch import Stopwatch
from utils.audio import play_sound
from utils.animation import Animation
from constants.graphics import SPRITE_SIZE
import os

COUNT_TO = 5
class Dynamite(Takeable):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='dynamite.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.clock = Stopwatch()
        self.clock.start()
        self.last_second = 0

        animation_dir = os.path.join(sprite_dir, 'animations', 'explosion')

        self.exploded = False

        self.explosion = Animation(
            animation_dir,
            refresh_interval=0.05,
            start_frame=0,
            size=SPRITE_SIZE,
            loop = False
        )

    
    def draw(self, screen, x, y):
        """ Draw current frame of fire animation """
        if not self.exploded:
            return super().draw(screen, x, y)
            
        
        pos = self.calculate_pos(x, y)

        frame = self.explosion.get_frame()

        screen.blit(frame, pos)

        if not self.explosion.has_more_frames():
            self.purge = True


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
            self.exploded = True


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