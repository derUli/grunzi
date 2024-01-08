""" Microwave which can be destroyed with dynamite """
from sprites.sprite import Sprite
import os 
from utils.animation import Animation
from constants.graphics import SPRITE_SIZE

class Microwave(Sprite):
    """ Microwave sprite class """

    def __init__(self, sprite_dir, cache, sprite='microwave.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False

        animation_dir = os.path.join(sprite_dir, 'animations', 'explosion')

        self.explode = False
        
        self.explosion = Animation(
            animation_dir,
            refresh_interval=0.08,
            start_frame=0,
            size=SPRITE_SIZE,
            loop = False
        )

    
    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        if not self.explode:
            return


        pos = self.calculate_pos(x, y)
        frame = self.explosion.get_frame()

        screen.blit(frame, pos)

        if not self.explosion.has_more_frames():
            self.purge = True