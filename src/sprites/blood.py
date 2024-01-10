""" Blood sprite """

from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable

class Blood(Takeable, InlineSprite):
    """ blood sprite class """

    def __init__(self, sprite_dir, cache, sprite='blood.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.blood_amount = 20
