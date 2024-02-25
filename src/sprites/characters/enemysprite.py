""" Player sprite class """

from arcade import FACE_RIGHT

from sprites.characters.sprite import Sprite
from sprites.characters.spritehealth import SpriteHealth

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 200
MOVE_DAMPING = 0.01

SIGHT_DISTANCE = 600
SIGHT_CHECK_RESOLUTION = 32

FADE_IN_MAX = 255
FADE_SPEED = 2

DAMAGE = 0


class EnemySprite(Sprite, SpriteHealth):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(center_x=center_x, center_y=center_y)
        self.damage = DAMAGE

        self.health = 100

    def draw_debug(self):
        return

    def update(self, player=None, scene=None, physics_engine=None):
        return
