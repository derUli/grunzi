import os
from typing import Optional

import arcade
from arcade import Texture

from sprites.items.item import Interactable
from sprites.sprite import Sprite

SWITCH_OFF = 0
SWITCH_ON = 1


class Switch(Sprite, Interactable):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            image_x: float = 0,
            image_y: float = 0,
            image_width: float = 0,
            image_height: float = 0,
            center_x: float = 0,
            center_y: float = 0,
            repeat_count_x: int = 1,  # Unused
            repeat_count_y: int = 1,  # Unused
            flipped_horizontally: bool = False,
            flipped_vertically: bool = False,
            flipped_diagonally: bool = False,
            hit_box_algorithm: Optional[str] = "Simple",
            hit_box_detail: float = 4.5,
            texture: Texture = None,
            angle: float = 0
    ):
        super().__init__(
            filename,
            scale,
            image_x,
            image_y,
        )

        path = os.path.dirname(filename)

        self.textures = [
            arcade.load_texture(os.path.join(path, 'off2.png')),
            arcade.load_texture(os.path.join(path, 'on2.png'))
        ]

        self._enabled = SWITCH_OFF

        self.texture = self.textures[self._enabled]

        self.check_initialized = False

    @property
    def enabled(self) -> int:
        return self._enabled

    @enabled.setter
    def enabled(self, value: int):
        self._enabled = value

    def on_interact(self, args):
        if self._enabled:
            return

        self._enabled = SWITCH_ON

        self.texture = self.textures[self.enabled]

        args.state.play_sound('switch')
