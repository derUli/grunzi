"""Backdrop sprite"""

import sprites.sprite
import random

GRAS_SPRITES = ['gras1.jpg', 'gras2.jpg', 'gras3.jpg', 'gras4.jpg', 'gras5.jpg', 'gras6.jpg']

class Backdrop(sprites.sprite.Sprite):

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        if not sprite:
            sprite = random.choice(GRAS_SPRITES)
        super().__init__(sprite_dir, cache, sprite)
