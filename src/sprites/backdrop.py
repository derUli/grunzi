"""Backdrop sprite"""

import sprites.sprite
import random

GRAS_SPRITES = ['gras1.jpg', 'gras2.jpg', 'gras3.jpg']


class Backdrop(sprites.sprite.Sprite):

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        if not sprite:
            sprite = random.choice(GRAS_SPRITES)
        super().__init__(sprite_dir, cache, sprite)
