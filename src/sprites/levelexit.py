""" Backdrop sprite """

from sprites.backdrop import Backdrop

class LevelExit(Backdrop):
    """ Backdrop sprite """

    def __init__(self, sprite_dir, cache, sprite='exit.jpg'):
        super().__init__(sprite_dir, cache, sprite)
