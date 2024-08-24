""" Slimer sprite class """
import os

import arcade
from arcade import FACE_RIGHT

from constants.collisions import COLLISION_ENEMY
from constants.layers import LAYER_NPC, check_collision_with_layers, LAYER_WALL, WALL_LAYERS
from sprites.characters.character import Character
from utils.physics import DEFAULT_FRICTION
from utils.sprite import random_position

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 300000
MOVE_DAMPING = 0.01
MASS = 0.05

SIGHT_DISTANCE = 1400
GRID_SIZE = 64

FADE_IN_MAX = 255
FADE_SPEED = 4

class Barrel(Character):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(filename, center_x, center_y)

        self.damping = MOVE_DAMPING
        self.force = MOVE_FORCE
        self.friction = DEFAULT_FRICTION
        self.fade_in = True

        if self.fade_in:
            self.alpha = 0

    def draw_overlay(self, args):
        if self._health < 100:
            self.draw_healthbar()

    def update(
            self,
            delta_time,
            args
    ):
        if self.dead:
            alpha = self.alpha - FADE_SPEED

            if alpha <= 0:
                alpha = 0
                self.remove_from_sprite_lists()

            self.alpha = alpha

            return

        if self.fade_in and self.alpha < FADE_IN_MAX:
            new_alpha = self.alpha + FADE_SPEED

            if new_alpha >= FADE_IN_MAX:
                new_alpha = FADE_IN_MAX
                self.fade_in = False

            self.alpha = new_alpha

            return

        if not arcade.has_line_of_sight(
                self.position,
                args.player.position,
                args.wall_spritelist,
                SIGHT_DISTANCE,
                GRID_SIZE
        ):
            return


        args.physics_engine.apply_force(self, (0, -self.force))

        explodes = False

        if arcade.check_for_collision(self, args.player):
            explodes = True

        for layer in WALL_LAYERS:
            if not layer in args.scene.name_mapping:
                break

            if arcade.check_for_collision_with_list(self, args.scene[layer]):
                explodes = True

        if explodes:
            # TODO: Explosion
            self.health = 0


def spawn_barrel(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    barrel = Barrel(
        filename=os.path.join(
            state.sprite_dir,
            'monster',
            'barrel',
            'barrel.png'
        ),
        center_x=rand_x,
        center_y=rand_y
    )

    if check_collision_with_layers(scene, barrel):
        return spawn_barrel(state, tilemap, scene, physics_engine)

    scene.add_sprite(LAYER_NPC, barrel)
    physics_engine.add_sprite(
        barrel,
        friction=barrel.friction,
        collision_type=COLLISION_ENEMY,
        mass=MASS,
        max_velocity=200,
        damping=barrel.damping
    )
