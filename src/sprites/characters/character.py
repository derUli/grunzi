""" Player sprite class """

from sprites.characters.spritehealth import SpriteHealth
from sprites.sprite import Sprite

DAMAGE = 0
HEALTH_FULL = 100


class Character(Sprite, SpriteHealth):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(center_x=center_x, center_y=center_y)
        self.damage = DAMAGE
        self.health = HEALTH_FULL

    def draw_debug(self):
        """ Draw debug overlays """
        return
