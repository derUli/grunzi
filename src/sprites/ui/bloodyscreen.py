import os

import PIL
import arcade.sprite
from PIL.Image import Resampling

FULL_ALPHA = 255
ONE_PERCENT_ALPHA = FULL_ALPHA / 100
COLOR_BLOOD = (156, 28, 28)


class BloodyScreen:
    def __init__(self):
        self.state = None
        self.sprite = None
        self._alpha = 0

    def setup(self, state):
        window = arcade.get_window()

        image = PIL.Image.open(
            os.path.join(state.ui_dir, 'blood.png')
        ).convert('RGBA').crop()

        # TODO: Bloody Screen in Klasse auslagern
        image = image.resize(
            window.size,
            resample=Resampling.BILINEAR
        )
        texture = arcade.texture.Texture(
            name='blood',
            image=image
        )

        self.sprite = arcade.sprite.Sprite(
            texture=texture,
            center_x=window.width / 2,
            center_y=window.height / 2
        )

        return self

    def update(self, health):
        # TODO: Fade to alpha value animation

        a = FULL_ALPHA - health * ONE_PERCENT_ALPHA
        self._alpha = a

    def draw(self):
        if self._alpha <= 0:
            return

        window = arcade.get_window()

        self.sprite.alpha = self._alpha
        self.sprite.draw()

        r, g, b = COLOR_BLOOD

        arcade.draw_rectangle_filled(
            window.width / 2,
            window.height / 2,
            window.width,
            window.height,
            (r, g, b, self._alpha)
        )
