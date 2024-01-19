""" Hammer sprite """

from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable


class Remote(Takeable, InlineSprite):
    """ Hammer sprite class """

    def __init__(self, sprite_dir, cache, sprite='remote.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)


    def draw_inline(self, screen, pos):
        """ draw sprite """
        screen.blit(self.sprite, pos)