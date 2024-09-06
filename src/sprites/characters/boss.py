""" Slimer sprite class """
import os

import arcade
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

EYE_OFFSET_X = 100
EYE_SPACING_X = 250
EYE_OFFSET_Y = 10

ALPHA_SPEED = 4
ALPHA_MAX = 255

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

        self.eye_file = os.path.join(os.path.dirname(filename), 'eye.png')
        self.eye1 = None
        self.eye2 = None
        self.spawn_sound = None
        self.triggered = False

    def update(self, delta_time, args):
        w, h = arcade.get_window().get_size()
        if not self.triggered and arcade.get_distance_between_sprites(self, args.player) < h:
            self.triggered = True

            self.spawn_sound = args.state.play_sound('boss', 'spawn')
            return

        if not self.triggered:
            return

        if self.alpha < ALPHA_MAX:
            alpha = self.alpha + ALPHA_SPEED

            if alpha > ALPHA_MAX:
                alpha = ALPHA_MAX

            self.alpha = alpha

        super().update(delta_time, args)

        self.eye1.center_x = self.center_x - EYE_OFFSET_X
        self.eye1.center_y = self.center_y - EYE_OFFSET_Y
        self.eye1.alpha = self.alpha

        self.eye2.center_x = self.eye1.center_x + EYE_SPACING_X
        self.eye2.center_y = self.eye1.center_y
        self.eye2.alpha = self.alpha

        if self.dead:
            # Fade out on death
            self.fade_destroy()

            # Complete level after boss killed
            if self.alpha <= 0:
                args.callbacks.on_complete()

    def setup(self, args):
        from constants.layers import LAYER_NPC

        self.remove_from_sprite_lists()

        args.scene.add_sprite(LAYER_NPC, self)

        args.physics_engine.add_sprite(
            self,
            mass=500,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            collision_type=COLLISION_ENEMY
        )


        self.eye1 = arcade.sprite.Sprite(filename=self.eye_file)
        args.scene.add_sprite(LAYER_NPC, self.eye1)

        self.eye2 = arcade.sprite.Sprite(filename=self.eye_file, flipped_horizontally=True)
        args.scene.add_sprite(LAYER_NPC, self.eye2)

        self.alpha = 0

    def draw_overlay(self, args):
        self.draw_healthbar()



