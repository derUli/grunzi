from typing import Optional

import arcade
from arcade import Texture, load_texture


class ScrollingBackdrop(arcade.sprite.Sprite):
    def __init__(
            self,
            filename: str = None,
    ):

        super().__init__(filename)

        self.change_x = 0