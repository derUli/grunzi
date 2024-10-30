import os

import PIL
import arcade
from PIL import ImageFilter
from PIL.Image import Resampling

from state.viewstate import ViewState
from utils.eastereggs import is_halloween, get_loading_screen_image_file
from utils.sprite import load_animated_gif
from utils.text import create_text

MARGIN = 10
PERCENTAGE_SPEED = 1
FONT_SIZE = 16
MAX_BLUR = 15


class LoadingScreen:
    def __init__(self):
        self.size = None

        self.time = 0

        self.onepercent = None
        self._percent = 0
        self._display_percentage = 0
        self.loading_animation = None
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

        self._percent = 0
        self._display_percentage = 0

        file = get_loading_screen_image_file()

        path = os.path.join(state.ui_dir, 'loading_screens', file)
        is_halloween()
        image = PIL.Image.open(path).convert('RGBA').crop()

        image = image.resize(
            arcade.get_window().get_size(),
            resample=state.settings.pil_resample
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
            size=(w, h),
            resample=state.settings.pil_resample
        )
        self.filmgrain.alpha = 18 * state.settings.filmgrain
        self.filmgrain.position = (w / 2, h / 2)

        self.loading_animation = arcade.load_animated_gif(os.path.join(state.animation_dir, 'loading.gif'))
        self.loading_animation.left = self.image.width - self.loading_animation.width - MARGIN
        self.loading_animation.bottom = MARGIN

        self.loading_text = create_text(
            _("Loading..."),
            font_size=FONT_SIZE,
            color=arcade.color.BLACK,
            align='left'
        )

        self.loading_text.x = w / 2 - self.loading_text.content_width / 2
        self.loading_text.y = MARGIN

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
        self.loading_animation.update_animation(delta_time)

    @property
    def completed(self):
        return self._display_percentage >= 100

    def draw(self, time=None):

        if not self.show:
            return

        self.image.draw()
        self.loading_text.draw()
        self.filmgrain.draw()
        self.loading_animation.draw()
