from typing import Optional

import arcade
from arcade import Texture, load_texture


class PlayerSprite(arcade.sprite.Sprite):
    def __init__(
            self,
            filename: str = None,
    ):

        super().__init__(filename)

        self.change_x = 0

        self.texture_right = self.texture

        self.texture_left = load_texture(
            filename,
            flipped_horizontally=True
        )

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.texture_left
        elif self.change_x > 0:
            self.texture = self.texture_right