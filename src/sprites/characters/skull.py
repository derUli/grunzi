""" Player sprite class """
import os

import arcade
import pyglet.clock
from arcade import FACE_RIGHT, FACE_LEFT, PymunkPhysicsEngine

from constants.collisions import COLLISION_ENEMY
from constants.layers import LAYER_NPC, check_collision_with_layers
from sprites.bullet.skullbullet import SkullBullet
from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL
from sprites.items.item import Useable
from utils.physics import DEFAULT_FRICTION
from utils.sprite import random_position

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 300
MOVE_DAMPING = 0.01

SIGHT_DISTANCE = 1000
GRID_SIZE = 64

FADE_IN_MAX = 255
FADE_SPEED = 4

SHOOT_DELTA = 1 / 5.5

PATH_FINDING_INTERVAL = 1


class Skull(Character, Useable):
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

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()

        w, h = args.map_size

        self.playing_field_left_boundary = self.left - w
        self.playing_field_right_boundary = self.right + w
        self.playing_field_top_boundary = self.top + h
        self.playing_field_bottom_boundary = self.bottom - h

        difference = arcade.get_distance_between_sprites(self, args.player)

        self.insight = difference < SIGHT_DISTANCE

        if not self.insight:
            return

        self.chasing = args.player

        if not self.chased:
            args.state.play_sound('screech')

            self.chased = True
            self.update_texture()

            pyglet.clock.schedule_interval_soft(self.update_move_path, 1 / 4, args.player, args.astar_barrier_list)

        if self.chasing:
            if not self.move_path:
                self.move_path = []

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

                args.physics_engine.apply_force(self, (force_x, force_y))

            self.shoot_time += delta_time

            if len(self.move_path) == 0:
                return

            if self.shoot_time < SHOOT_DELTA:
                return

            if not arcade.has_line_of_sight(
                    self.position,
                    args.player.position,
                    args.wall_spritelist,
                    SIGHT_DISTANCE,
                    GRID_SIZE
            ):
                self.shoot_time = 0
                return

            bullet = SkullBullet(
                6,
                color=arcade.csscolor.RED,
                hurt=args.state.difficulty.skull_hurt
            )

            bullet.setup(
                source=self,
                physics_engine=args.physics_engine,
                scene=args.scene,
                state=args.state,
                target=args.player
            )

            self.shoot_time = 0

    def update_move_path(self, delta, player, astar_barrier_list):
        if not self.insight or self.dead:
            return

        move_path = arcade.astar_calculate_path(
            self.position,
            (player.center_x, player.center_y),
            astar_barrier_list,
            diagonal_movement=True
        )

        if move_path:
            self.move_path = move_path


def spawn_skull(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    skull = Skull(
        filename=os.path.join(
            state.sprite_dir,
            'monster',
            'skull',
            'skull.png'
        ),
        center_x=rand_x,
        center_y=rand_y
    )

    if check_collision_with_layers(scene, skull):
        return spawn_skull(state, tilemap, scene, physics_engine)

    scene.add_sprite(LAYER_NPC, skull)
    physics_engine.add_sprite(
        skull,
        friction=skull.friction,
        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
        collision_type=COLLISION_ENEMY,
        max_velocity=200,
        damping=skull.damping
    )
    return
