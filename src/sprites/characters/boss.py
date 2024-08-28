""" Slimer sprite class """
from arcade import FACE_RIGHT, PymunkPhysicsEngine

from constants.collisions import COLLISION_ENEMY
from sprites.characters.character import Character

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MASS = 0.1
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1
FORCE_MOVE = 300

SIGHT_DISTANCE = 1400
COLLISION_CHECK_DISTANCE = 200
GRID_SIZE = 64

FADE_IN_MAX = 255
FADE_SPEED = 4


class Boss(Character):
    def __init__(
            self,
            filename: str | None = None,
            image_x=0,
            image_y=0,
            image_width=None,
            image_height=None,
            flipped_horizontally=False,
            flipped_vertically=False,
            flipped_diagonally=False,
            hit_box_algorithm=None,
            hit_box_detail=None,
            scale=1.0,
            center_x=None,
            center_y=None
    ):
        super().__init__(filename, center_x=center_x, center_y=center_y)


    def setup(self, args):
        from constants.layers import LAYER_NPC

        args.scene.add_sprite(LAYER_NPC, self)

        args.physics_engine.add_sprite(
            self,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            collision_type=COLLISION_ENEMY
        )

    def draw_overlay(self, args):
        self.draw_healthbar()

