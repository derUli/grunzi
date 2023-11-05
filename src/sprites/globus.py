""" Racoon character """
import os

import constants.direction
import constants.graphics
import sprites.sprite
from utils.animation import Animation

class Globus(sprites.sprite.Sprite):
    """ Fire character class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """

        super().__init__(sprite_dir, cache, 'gras1.jpg')
        sprite_dir = os.path.join(sprite_dir, 'animations', 'globus')

        w, h = constants.graphics.SPRITE_SIZE

        self.animation = Animation(
            sprite_dir,
            refresh_interval=0.1,
            size=constants.graphics.SPRITE_SIZE)
        self.walkable = False

    def draw(self, screen, x, y):
        """ Draw current frame of fire animation """
        frame = self.animation.get_frame()
        pos = self.calculate_pos(x, y)
        screen.blit(frame, pos)
