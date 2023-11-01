"""Backdrop sprite"""

import sprites.sprite


class Backdrop(sprites.sprite.Sprite):

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'gras.jpg')
