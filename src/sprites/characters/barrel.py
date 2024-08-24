""" Slimer sprite class """
import os

import arcade
from arcade import FACE_RIGHT, PymunkPhysicsEngine, SpriteList

from constants.collisions import COLLISION_ENEMY
from constants.layers import LAYER_NPC, check_collision_with_layers
from sprites.characters.character import Character
from sprites.items.item import Useable
from utils.physics import DEFAULT_FRICTION
from utils.sprite import random_position

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 300
MOVE_DAMPING = 0.01

SIGHT_DISTANCE = 1400
GRID_SIZE = 64

FADE_IN_MAX = 255
FADE_SPEED = 4

SHOOT_DELTA = 1

PATH_FINDING_INTERVAL = 1


class Barrel(Character):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(filename, center_x, center_y)

        self.damping = MOVE_DAMPING
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
        max_velocity=200,
        damping=barrel.damping
    )
