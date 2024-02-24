""" Player sprite class """
import os

import arcade
from arcade import FACE_RIGHT, FACE_LEFT

from utils.physics import DEFAULT_FRICTION

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
PLAYER_MOVE_FORCE = 1000
PLAYER_DAMPING = 0.2

SIGHT_DISTANCE = 500
SIGHT_CHECK_RESOLUTION = 2

class SkullSprite(arcade.sprite.Sprite):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(center_x=center_x, center_y = center_y)

        self.move_force = PLAYER_MOVE_FORCE
        self.damping = PLAYER_DAMPING

        dirname = os.path.join(os.path.dirname(filename))

        self.skull_off = self.textures = arcade.load_texture_pair(
            os.path.join(dirname, 'skull.png')
        )
        self.skull_on = self.textures = arcade.load_texture_pair(
            os.path.join(dirname, 'skull2.png')
        )

        self.chasing = False

        self.friction = DEFAULT_FRICTION

        self.face = DEFAULT_FACE
        self.textures = None

        self.update_texture()

    def update_texture(self):
        if self.chasing:
            self.textures = self.skull_on
        else:
            self.textures = self.skull_off

        self.texture = self.textures[self.face - 1]

    def update(self, player = None, walls = None):

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()

        if not player or not walls:
            return

        self.chasing = arcade.has_line_of_sight(player.position,
            self.position,
            walls=walls,
            check_resolution=SIGHT_CHECK_RESOLUTION,
            max_distance= SIGHT_DISTANCE
        )

        astar_barrier_list = arcade.AStarBarrierList(walls)


        print(arcade.astar_calculate_path(self.position,
                                    player.position,
                                    astar_barrier_list,
                                    diagonal_movement=False))

        self.update_texture()