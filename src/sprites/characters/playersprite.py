import os

import arcade
from arcade import FACE_RIGHT, FACE_LEFT

STATE_DEFAULT = 'default'
STATE_GUN = 'gun'

DEFAULT_FACE = FACE_RIGHT

# Physics force used to move the player. Higher number, faster accelerating.
PLAYER_MOVE_FORCE = 1000

PLAYER_DAMPING = 0.2

class PlayerSprite(arcade.sprite.Sprite):
    def __init__(
            self,
            filename: str = None,
    ):
        super().__init__()

        path = os.path.dirname(filename)
        self.move_force = PLAYER_MOVE_FORCE
        self.damping = PLAYER_DAMPING

        self.pig_textures = {
            STATE_DEFAULT: {
                FACE_RIGHT: arcade.load_texture(
                    os.path.join(path, 'pig.png')
                ),
                FACE_LEFT: arcade.load_texture(
                    os.path.join(path, 'pig.png'),
                    flipped_horizontally=True
                )
            }
        }

        self.state = STATE_DEFAULT
        self.face = DEFAULT_FACE
        self.texture = self.pig_textures[self.state][self.face]

    def update_texture(self):
        self.texture = self.pig_textures[self.state][self.face]

    def update(self):

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()
