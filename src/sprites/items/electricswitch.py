import os
from typing import Optional

import arcade
import pyglet
from arcade import Texture

from sprites.sprite import Sprite

SWITCH_OFF = 0
SWITCH_ON = 1


class ElectricSwitch(Sprite):
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
            arcade.load_texture(os.path.join(path, 'off1.jpg')),
            arcade.load_texture(os.path.join(path, 'on1.jpg'))
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

    def update(
            self,
            delta_time,
            args
    ):
        if not self.check_initialized:
            self.check_initialized = True
            pyglet.clock.schedule_interval_soft(self.check_cone, 1 / 6, args.scene)

    def check_cone(self, delta_time: float, scene) -> None:
        from constants.layers import LAYER_CONES

        collision = arcade.check_for_collision_with_list(
            self,
            scene[LAYER_CONES]
        )

        if len(collision) == 1:
            self._enabled = SWITCH_ON
        else:
            self._enabled = SWITCH_OFF

        self.texture = self.textures[self._enabled]
