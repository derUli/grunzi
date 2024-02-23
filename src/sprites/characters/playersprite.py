import os
from typing import Optional

import arcade
from arcade import Texture, load_texture, FACE_RIGHT, FACE_LEFT

STATE_DEFAULT = 'default'
STATE_GUN = 'gun'

DEFAULT_FACE = FACE_RIGHT

class PlayerSprite(arcade.sprite.Sprite):
    def __init__(
            self,
            filename: str = None,
    ):
        super().__init__()

        path = os.path.dirname(filename)

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

        self.change_x = 0


    def update_texture(self):
        self.texture = self.pig_textures[self.state][self.face]

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()