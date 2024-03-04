from typing import Optional

import PIL
import arcade

from sprites.items.item import Item

SCALE = 0.6


class Coin(arcade.sprite.Sprite, Item):
    def __init__(
            self,
            filename: Optional[str] = None,
            image_x=0,
            image_y=0,
            image_width=1,
            image_height=1,
            flipped_horizontally=False,
            flipped_vertically=False,
            flipped_diagonally=False,
            hit_box_algorithm=None,
            hit_box_detail=None,
            scale=1.0,
            center_x=None,
            center_y=None
    ):
        self.filename = filename

        self.image = PIL.Image.open(filename).convert('RGBA').crop()

        texture = arcade.texture.Texture(name='coin', image=self.image)

        super().__init__(
            texture=texture,
            scale=SCALE,
            image_x=image_x,
            image_y=image_y,
            image_width=image_width,
            image_height=image_height,
            flipped_horizontally=flipped_horizontally,
            flipped_vertically=flipped_vertically,
            flipped_diagonally=flipped_diagonally,
            hit_box_algorithm=hit_box_algorithm,
            hit_box_detail=hit_box_detail,
            center_x=center_x,
            center_y=center_y
        )

        self.center_x, center_y