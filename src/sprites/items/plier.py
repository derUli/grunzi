from typing import Optional

import PIL
import arcade

from sprites.items.item import Item, Fence


class Plier(arcade.sprite.Sprite, Item):
    def __init__(
            self,
            filename: Optional[str] = None,
            image_x=0,
            image_y=0,
            image_width=None,
            image_height=None,
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

        texture = arcade.texture.Texture(name='plier', image=self.image)
        super().__init__(
            texture=texture,
            scale=scale,
            image_x=image_x,
            image_y=image_y,
        )

    def on_use(self, b, state):
        if isinstance(b, Fence):
            b.remove_from_sprite_lists()

            state.sounds['tools']['plier'].play()