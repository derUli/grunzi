import PIL
import arcade
import os
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

        for i in range(0, 1):
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
        for sprite in self.spritelist:
            x, y = args.player.position
            x1, x2, w, h = args.camera.viewport

            if x < w / 2:
                x = w / 2

            if y < h / 2:
                y = h / 2

            sprite.position = (x, y)

    def draw(self):
        self.spritelist.draw()
