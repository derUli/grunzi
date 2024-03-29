import logging
from typing import Optional

import PIL
import arcade
from arcade import AnimatedTimeBasedSprite

from sprites.sprite import Sprite


class Item(Sprite):
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

        texture = arcade.texture.Texture(name=filename, image=self.image)
        super().__init__(
            texture=texture,
            scale=scale,
            image_x=image_x,
            image_y=image_y,
        )

    def on_use(self, b, state=None, handlers=None):
        logging.info(f"Use item {self} with {b}")

    def copy(self):
        logging.debug('Copy not implemented')
        return self


class Useable:
    pass


class Fence(Sprite, Useable):
    pass


class PiggyBank(Sprite, Useable):
    pass


class Jeep(Sprite, Useable):
    pass


class Water(AnimatedTimeBasedSprite):
    pass
