""" Landmine """
import os

from sprites.sprite import Sprite
from utils.animation import Animation
from constants.graphics import SPRITE_SIZE
from random import randint


LANDMINE_HURT_MIN = 30
LANDMINE_HURT_MAX = 80

class LandMine(Sprite):    
    """ Landmine """

    def __init__(self, sprite_dir, cache, sprite='landmine.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        
        self.walkable = True

        animation_dir = os.path.join(sprite_dir, 'animations', 'explosion')

        # Damage can be statically defined
        self.attributes = {
            'damage': None 
        }

        self.explosion = Animation(
            animation_dir,
            refresh_interval=0.01,
            start_frame=0,
            size=SPRITE_SIZE,
            loop=False
        )

        self.exploded = False


    def draw(self, screen, x, y):
        """ Draw """
        super().draw(screen, x, y)

        if not self.exploded:
            return

        pos = self.calculate_pos(x, y)
        frame = self.explosion.get_frame()

        screen.blit(frame, pos)

        if not self.explosion.has_more_frames():
            self.purge = True


    def handle_interact(self, element):
        """ Explode on enter """
        if not element:
            return

        self.exploded = True

        damage = self.attributes['damage']

        # If damage is not statically defined randomize damage
        if not damage:
            damage = randint(LANDMINE_HURT_MIN, LANDMINE_HURT_MAX)
        
        element.state.hurt(damage)
