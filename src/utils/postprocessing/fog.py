import os
from typing import Self

import PIL
import arcade
from PIL import ImageOps
from PIL.Image import Resampling

from state.argscontainer import ArgsContainer
from utils.postprocessing.effect import Effect

DEFAULT_ALPHA = 180

MOVE_SPEED = 0.33


class Fog(Effect):
    def setup(self, args: ArgsContainer) -> Self:
        """
        Setup fog effect
        @param args: ArgsContainer
        @return: Self
        """

        image = PIL.Image.open(
            os.path.join(args.state.image_dir, 'postprocessing', 'fog.png')
        ).convert('RGBA').crop()

        size = arcade.get_window().get_size()

        self.spritelist.clear()

        image = image.resize(
            size,
            resample=Resampling.BILINEAR
        )

        image_mirror = ImageOps.mirror(image)

        x = 0

        max_x = args.tilemap.width + image.width

        i = 0

        flip = False

        while x < max_x or flip:
            i += 1

            img = image

            if flip:
                img = image_mirror

            flip = not flip

            texture = arcade.texture.Texture(
                name=f"Fog{i}",
                image=img
            )

            sprite = arcade.sprite.Sprite(texture=texture)
            sprite.left = x
            sprite.top = 0

            sprite.alpha = DEFAULT_ALPHA
            self.spritelist.append(sprite)

            x += sprite.width

        return self

    def update(self, delta_time: float, args: ArgsContainer) -> None:
        for sprite in self.spritelist:
            x, y = args.player.position

            sprite.left -= MOVE_SPEED

            w, h = arcade.get_window().get_size()

            if y < h * 0.5:
                y = h * 0.5

            sprite.center_y = y

            if sprite.right <= 0:
                sprite.right = ((len(self.spritelist)) * sprite.width) - abs(sprite.right)

    def draw(self) -> None:
        """ Draw fog """

        self.spritelist.draw()
