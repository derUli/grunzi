""" Player sprite class """
import os

import arcade
from arcade import FACE_RIGHT, FACE_LEFT, PymunkPhysicsEngine

from constants.collisions import COLLISION_ENEMY
from constants.layers import LAYER_WALL, all_layers, LAYER_ENEMIES
from sprites.bullet.skullbullet import SkullBullet
from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL
from sprites.items.item import Useable
from utils.physics import DEFAULT_FRICTION
from utils.sprite import random_position
from window.gamewindow import UPDATE_RATE

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 200
MOVE_DAMPING = 0.01

SIGHT_DISTANCE = 600
SIGHT_CHECK_RESOLUTION = 64

FADE_IN_MAX = 255
FADE_SPEED = 5

DAMAGE = 5
GRID_SIZE = 64

SHOOT_DELTA = UPDATE_RATE * 10


class SkullSprite(Character, Useable):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0,
    ):
        super().__init__(center_x=center_x, center_y=center_y)

        self.move_force = MOVE_FORCE
        self.damping = MOVE_DAMPING

        self.health = HEALTH_FULL
        self._died = False

        dirname = os.path.join(os.path.dirname(filename))

        self.skull_off = self.textures = arcade.load_texture_pair(
            os.path.join(dirname, 'skull.png')
        )
        self.skull_on = self.textures = arcade.load_texture_pair(
            os.path.join(dirname, 'skull2.png')
        )

        self.chasing = None
        self.chased = False
        self.playing_field_left_boundary = 0
        self.playing_field_right_boundary = 0
        self.playing_field_top_boundary = 0
        self.playing_field_bottom_boundary = 0

        self.friction = DEFAULT_FRICTION
        self.move_path = []
        self.face = DEFAULT_FACE
        self.textures = None
        self.update_texture()
        self.astar_barrier_list = None
        self.damage = DAMAGE
        self.fade_in = True

        self.shoot_time = 0

        if self.fade_in:
            self.alpha = 0

    def update_texture(self):
        if self.chasing:
            self.textures = self.skull_on
        else:
            self.textures = self.skull_off

        self.texture = self.textures[self.face - 1]

    def draw_overlay(self):
        self.draw_healthbar()

    def draw_debug(self):
        if not self.insight:
            return

        arcade.draw_lrtb_rectangle_outline(
            self.playing_field_left_boundary,
            self.playing_field_right_boundary,
            self.playing_field_top_boundary,
            self.playing_field_bottom_boundary,
            color=arcade.csscolor.RED
        )

        if self.move_path:
            arcade.draw_line_strip(self.move_path, arcade.color.RED, 2)

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

        if self.fade_in and self.alpha < FADE_IN_MAX:
            new_alpha = self.alpha + FADE_SPEED

            if new_alpha >= FADE_IN_MAX:
                new_alpha = FADE_IN_MAX
                self.fade_in = False

            self.alpha = new_alpha

            return

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()

        self.playing_field_left_boundary = self.left - SIGHT_DISTANCE
        self.playing_field_right_boundary = self.right + SIGHT_DISTANCE
        self.playing_field_top_boundary = self.top + SIGHT_DISTANCE
        self.playing_field_bottom_boundary = self.bottom - SIGHT_DISTANCE

        difference = arcade.get_distance_between_sprites(self, player)

        self.insight = difference < SIGHT_DISTANCE

        if not self.insight:
            return

        if arcade.has_line_of_sight(
                player.position,
                self.position,
                walls=scene[LAYER_WALL],
                check_resolution=SIGHT_CHECK_RESOLUTION,
                max_distance=SIGHT_DISTANCE
        ):
            self.chasing = player

            if not self.chased:
                state.play_sound('screech')
            self.chased = True
            self.update_texture()

        if self.chasing:
            if not self.astar_barrier_list:
                self.update_barrier_list(scene)

            move_path = arcade.astar_calculate_path(
                self.position,
                (player.center_x, player.center_y),
                self.astar_barrier_list,
                diagonal_movement=True
            )

            if move_path:
                self.move_path = move_path

            for path in self.move_path:

                x1, y1 = self.position
                x2, y2 = path

                force_x, force_y = 0, 0

                if y2 > y1:
                    force_y = self.move_force
                if y1 > y2:
                    force_y = -self.move_force
                if x2 > x1:
                    force_x = self.move_force
                if x1 > x2:
                    force_x = -self.move_force

                physics_engine.apply_force(self, (force_x, force_y))

            self.shoot_time += delta_time

            if self.shoot_time < SHOOT_DELTA:
                return

            bullet = SkullBullet(6, color=arcade.csscolor.RED)
            bullet.setup(
                source=self,
                physics_engine=physics_engine,
                scene=scene,
                state=state,
                target=player
            )
            self.update_barrier_list(scene)
            self.shoot_time = 0

    def update_barrier_list(self, scene):
        self.astar_barrier_list = arcade.AStarBarrierList(
            moving_sprite=self,
            blocking_sprites=scene[LAYER_WALL],
            grid_size=GRID_SIZE,
            left=int(self.playing_field_left_boundary),
            right=int(self.playing_field_right_boundary),
            bottom=int(self.playing_field_bottom_boundary),
            top=int(self.playing_field_top_boundary)
        )


def spawn_skull(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    skull = SkullSprite(
        filename=os.path.join(
            state.sprite_dir,
            'monster',
            'skull',
            'skull.png'
        ),
        center_x=rand_x,
        center_y=rand_y
    )

    if arcade.check_for_collision_with_list(skull, all_layers(scene)):
        return

    scene.add_sprite(LAYER_ENEMIES, skull)
    physics_engine.add_sprite(
        skull,
        friction=skull.friction,
        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
        collision_type=COLLISION_ENEMY,
        max_velocity=200,
        damping=skull.damping
    )
