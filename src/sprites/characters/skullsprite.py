""" Player sprite class """
import os

import arcade
from arcade import FACE_RIGHT, FACE_LEFT

from utils.physics import DEFAULT_FRICTION

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
PLAYER_MOVE_FORCE = 1000
PLAYER_DAMPING = 0.2

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
        self.textures = arcade.load_texture_pair(filename)
        self.friction = DEFAULT_FRICTION

        self.face = DEFAULT_FACE
        self.texture = self.textures[self.face - 1]

    def update_texture(self):
        self.texture = self.textures[self.face - 1]

    def update(self):

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()
