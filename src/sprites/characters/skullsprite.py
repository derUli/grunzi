""" Player sprite class """
import os

import arcade
from arcade import FACE_RIGHT, FACE_LEFT

import views.game
from sprites.characters.enemysprite import EnemySprite
from sprites.characters.spritehealth import HEALTH_FULL, HEALTH_EMPTY
from utils.physics import DEFAULT_FRICTION

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 200
MOVE_DAMPING = 0.01

SIGHT_DISTANCE = 600
SIGHT_CHECK_RESOLUTION = 32

FADE_IN_MAX = 255
FADE_SPEED = 5

DAMAGE = 1
GRID_SIZE = 64


class SkullSprite(EnemySprite):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0,
    ):
        super().__init__(center_x=center_x, center_y=center_y)

        self.move_force = MOVE_FORCE
        self.damping = MOVE_DAMPING

        self._scale = 1

        self.health = HEALTH_FULL

        dirname = os.path.join(os.path.dirname(filename))

        self.skull_off = self.textures = arcade.load_texture_pair(
            os.path.join(dirname, 'skull.png')
        )
        self.skull_on = self.textures = arcade.load_texture_pair(
            os.path.join(dirname, 'skull2.png')
        )

        self.chasing = None

        self.playing_field_left_boundary = 0
        self.playing_field_right_boundary = 0
        self.playing_field_top_boundary = 0
        self.playing_field_bottom_boundary = 0

        self.friction = DEFAULT_FRICTION
        self.move_path = None
        self.face = DEFAULT_FACE
        self.textures = None
        self.update_texture()
        self.astar_barrier_list = None
        self.damage = DAMAGE
        self.fade_in = True

        if self.fade_in:
            self.alpha = 0

    def update_texture(self):
        if self.chasing:
            self.textures = self.skull_on
        else:
            self.textures = self.skull_off

        self.texture = self.textures[self.face - 1]

    def draw_overlay(self):
        if not self.insight:
            return
        one_percent = self.width / 100
        width = round(one_percent * self.health)
        height = 4

        top = self.top + height * 2
        right = self.left + width

        a = self.alpha

        if a > 50:
            a = 50

        r, g, b = arcade.color.BLACK
        arcade.draw_line(self.left, top, self.right, top, line_width=height, color=(r, g, b, a))

        r, g, b = arcade.color.RED
        arcade.draw_line(self.left, top, right, top, line_width=height, color=(r, g, b, self.alpha))

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

    def update(self, player=None, scene=None, physics_engine=None):
        if self.health <= HEALTH_EMPTY:
            self.remove_from_sprite_lists()
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
                walls=scene[views.game.SPRITE_LIST_WALL],
                check_resolution=SIGHT_CHECK_RESOLUTION,
                max_distance=SIGHT_DISTANCE
        ):
            self.chasing = player
            self.update_texture()
        else:
            self.chasing = None
            self.update_texture()

        if self.chasing:
            if not self.astar_barrier_list:
                self.astar_barrier_list = arcade.AStarBarrierList(
                    moving_sprite=self,
                    blocking_sprites=scene[views.game.SPRITE_LIST_WALL],
                    grid_size=GRID_SIZE,
                    left=int(self.playing_field_left_boundary),
                    right=int(self.playing_field_right_boundary),
                    bottom=int(self.playing_field_bottom_boundary),
                    top=int(self.playing_field_top_boundary)
                )

            move_path = arcade.astar_calculate_path(
                self.position,
                (player.center_x, player.center_y),
                self.astar_barrier_list,
                diagonal_movement=True
            )

            if not move_path:
                return

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
