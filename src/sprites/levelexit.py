""" Backdrop sprite """

from sprites.backdrop import Backdrop

GRAS_SPRITES = ['gras1.jpg', 'gras2.jpg', 'gras3.jpg']


class LevelExit(Backdrop):
    """ Backdrop sprite """

    def __init__(self, sprite_dir, cache, sprite=None):
        super().__init__(sprite_dir, cache, sprite)

    def draw(self, screen, x, y):
        return
