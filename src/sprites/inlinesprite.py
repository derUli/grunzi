""" Wall sprite """

from sprites.sprite import Sprite


class InlineSprite(Sprite):
    """ Takeable sprite class """

    def __init__(self, sprite_dir, cache, sprite='coin.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
