import os

import PIL
import arcade
from PIL import ImageFilter
from PIL.Image import Resampling

from state.viewstate import ViewState
from utils.sprite import load_animated_gif
from utils.text import create_text

MARGIN = 5
PERCENTAGE_SPEED = 1
FONT_SIZE = 16
MAX_BLUR = 20

class LoadingScreen:
    def __init__(self):
        self.size = None

        self.loading_text = None
        self.time = 0

        self.onepercent = None
        self._percent = 0
        self._display_percentage = 0

        self.bar_height = 0

        self.show = False
        self.blur = MAX_BLUR
        self.image = None
        self.original_image = None
        self.filmgrain = None

    def setup(self, state: ViewState, size: tuple, show=False):
        self.show = show

        w, h = size
        self.size = size

        self.onepercent = w / 100

        self.loading_text = create_text(
            _("Loading..."),
            font_size=FONT_SIZE,
            color=arcade.color.BLACK,
            align='left'
        )

        self.bar_height = self.loading_text.content_height + (MARGIN * 2)

        self._percent = 0
        self._display_percentage = 0

        self.loading_text.x = w / 2 - self.loading_text.content_width / 2
        self.loading_text.y = MARGIN

        path = os.path.join(state.ui_dir, 'loading.jpg')
        image = PIL.Image.open(path).convert('RGBA').crop()

        image = image.resize(
            arcade.get_window().get_size(),
            resample=Resampling.BILINEAR
        )

        self.original_image = image
        self.blur = MAX_BLUR

        image = self.original_image.filter(
            ImageFilter.GaussianBlur(self.blur)
        )

        texture = arcade.texture.Texture(
            name=f"loading-{self.blur}",
            image=image
        )

        sprite = arcade.sprite.Sprite(
            texture=texture
        )
        sprite.position = (w / 2, h / 2)

        self.image = sprite

        self.filmgrain = load_animated_gif(
            os.path.join(state.animation_dir, 'grain.gif'),
            (w, h)
        )
        self.filmgrain.alpha = 40
        self.filmgrain.position = (w / 2, h / 2)

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, value):
        if value <= 0:
            value = 0

        if value > 100:
            value = 100

        self._percent = value

    def update(self, delta_time: float):
        if not self.show:
            return

        if self._percent > self._display_percentage:
            self._display_percentage += PERCENTAGE_SPEED

        elif self._percent < self._display_percentage:
            self._display_percentage -= PERCENTAGE_SPEED

        blur = MAX_BLUR - int(self._display_percentage * (MAX_BLUR / 100))

        if blur != self.blur:
            self.blur = blur
            texture = arcade.texture.Texture(
                image=self.original_image.filter(
                    ImageFilter.GaussianBlur(self.blur),
                ),
                name=f"radius-{self.blur}"
            )

            image = arcade.sprite.Sprite(texture=texture)
            image.position = self.image.position
            self.image = image

        self.filmgrain.update_animation(delta_time)
    @property
    def completed(self):
        return self._display_percentage >= 100

    def draw(self, time=None):

        if not self.show:
            return

        w, h = self.size

        self.image.draw()
        self.filmgrain.draw()

        arcade.draw_rectangle_filled(
            w / 2,
            self.bar_height / 2,
            w,
            self.bar_height,
            arcade.csscolor.PINK
        )

        bar_width = self._display_percentage * self.onepercent

        arcade.draw_rectangle_filled(
            bar_width / 2,
            self.bar_height / 2,
            bar_width,
            self.bar_height,
            arcade.csscolor.HOTPINK
        )

        self.loading_text.draw()
