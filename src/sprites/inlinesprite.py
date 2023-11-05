""" Wall sprite """

from sprites.sprite import Sprite


class InlineSprite(Sprite):
    """ Takeable sprite class """

    def __init__(self, sprite_dir, cache, sprite='coin.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.inline_sprite = self.sprite.copy().convert_alpha()

    def draw_inline(self, screen, pos):
        """ draw sprite """
        screen.blit(self.inline_sprite, pos)