import os

import PIL
import arcade
from PIL import ImageOps
from PIL.Image import Resampling

from typing import Self
from utils.postprocessing.effect import Effect
from state.argscontainer import ArgsContainer

DEFAULT_ALPHA = 180


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

        max_x = args.tilemap.width

        i = 0

        while x < max_x:
            i += 1

            img = image
            if i % 2 == 0:
                img = image_mirror

            texture = arcade.texture.Texture(
                name=f"Fog{i}",
                image=img
            )

            sprite = arcade.sprite.Sprite(texture=texture)
            sprite.left = x
            sprite.center_y = sprite.height / 2

            sprite.alpha = DEFAULT_ALPHA
            self.spritelist.append(sprite)

            x += sprite.width

        return self

    def update(self, delta_time: float, args: ArgsContainer) -> None:
        for sprite in self.spritelist:
            x, y = args.player.position
            sprite.center_y = y

    def draw(self) -> None:
        """ Draw fog """

        self.spritelist.draw()
