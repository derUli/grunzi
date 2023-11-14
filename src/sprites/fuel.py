""" Wall sprite """
from sprites.inlinesprite import InlineSprite
from sprites.takeable import Takeable


class Fuel(Takeable, InlineSprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='fuel.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.inline_sprite = self.sprite.copy().convert_alpha()

    def draw_inline(self, screen, pos):
        """ draw sprite """
        screen.blit(self.inline_sprite, pos)