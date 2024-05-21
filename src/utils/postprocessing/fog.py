import os

import PIL
import arcade
from PIL import ImageOps
from PIL.Image import Resampling

from utils.postprocessing.effect import Effect

DEFAULT_ALPHA = 180
MOVE_SPEED_DEFAULT = 0.2
MOVE_SPEED_WALK = 1.0


class Fog(Effect):
    def setup(self, args):

        image = PIL.Image.open(
            os.path.join(args.state.image_dir, 'postprocessing', 'fog.png')
        ).convert('RGBA').crop()

        size = arcade.get_window().get_size()

        self.spritelist.clear()

        image = image.resize(
            size,
            resample=Resampling.BILINEAR
        )

        x = 0

        for i in range(0, 2):
            if i == 1:
                image = ImageOps.mirror(image)

            texture = arcade.texture.Texture(
                name=f"Fog{i}",
                image=image
            )

            sprite = arcade.sprite.Sprite(texture=texture)
            sprite.center_x = x
            sprite.center_y = sprite.height / 2

            sprite.alpha = DEFAULT_ALPHA
            self.spritelist.append(sprite)

            x += sprite.width
        return self

    def update(self, delta_time, args):
        w, h = arcade.get_window().get_size()

        for sprite in self.spritelist:

            if sprite.right <= 0:
                sprite.left = w + sprite.right

            speed = MOVE_SPEED_DEFAULT

            if args.player.walking:
                speed = MOVE_SPEED_WALK * args.player.modifier

            sprite.center_x -= speed

    def draw(self):
        self.spritelist.draw()
