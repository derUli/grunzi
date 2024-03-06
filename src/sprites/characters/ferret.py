""" Player sprite class """
import os

import arcade
from arcade import FACE_RIGHT, PymunkPhysicsEngine

from constants.collisions import COLLISION_ENEMY, COLLISION_FERRET
from constants.layers import all_layers, LAYER_ENEMIES
from sprites.characters.enemysprite import EnemySprite
from sprites.characters.spritehealth import HEALTH_FULL, HEALTHBAR_FREN_COLOR
from utils.sprite import random_position

FADE_SPEED = 5
DEFAULT_FACE = FACE_RIGHT
MOVE_DAMPING = 0.01

class Ferret(EnemySprite):
    def __init__(
            self,
            filename: str = None,
            center_x = 0,
            center_y = 0
    ):
        super().__init__(filename, center_x=center_x, center_y=center_y)

        self.textures = arcade.load_texture_pair(filename)

        self.texture = self.textures[0]
        self.health = HEALTH_FULL
        self._died = False

        self.damping = MOVE_DAMPING

    def draw_overlay(self):
        self.draw_healthbar(HEALTHBAR_FREN_COLOR)

    def draw_debug(self):
        pass

    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        if self.dead:
            alpha = self.alpha - FADE_SPEED

            if alpha <= 0:
                alpha = 0
                self.remove_from_sprite_lists()

            self.alpha = alpha

            return


def spawn_ferret(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    ferret = Ferret(
        filename=os.path.join(state.sprite_dir, 'char', 'ferret.png'),
        center_x=rand_x,
        center_y=rand_y
    )

    if arcade.check_for_collision_with_list(ferret, all_layers(scene)):
        return spawn_ferret(state, tilemap, scene, physics_engine)

    scene.add_sprite(LAYER_ENEMIES, ferret)
    physics_engine.add_sprite(
        ferret,
        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
        collision_type=COLLISION_FERRET
    )