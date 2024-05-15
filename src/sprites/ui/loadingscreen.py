import arcade

from state.viewstate import ViewState
from utils.text import create_text, MEDIUM_FONT_SIZE

MARGIN = 5
PERCENTAGE_SPEED = 1


class LoadingScreen:
    def __init__(self):
        self.size = None
        self.shadertoy = None

        self.loading_text = None
        self.time = 0

        self.onepercent = None
        self._percent = 0
        self._display_percentage = 0

        self.bar_height = 0

        self.show = False

    def setup(self, state: ViewState, size: tuple, show=False):
        self.show = show
        if state.settings.shaders:
            self.shadertoy = state.load_shader(size, 'gameover')

        w, h = size
        self.size = size

        self.onepercent = w / 100

        self.loading_text = create_text(
            _("Loading..."),
            font_size=MEDIUM_FONT_SIZE,
            color=arcade.color.BLACK,
            align='left'
        )

        self.bar_height = self.loading_text.content_height + (MARGIN * 2)

        self._percent = 0
        self._display_percentage = 0

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

    def update(self):
        if not self.show:
            return

        if self._percent > self._display_percentage:
            self._display_percentage += PERCENTAGE_SPEED

        elif self._percent < self._display_percentage:
            self._display_percentage -= PERCENTAGE_SPEED

    @property
    def completed(self):
        return self._display_percentage >= 100

    def draw(self, time=None):

        if not self.show:
            return

        if self.shadertoy:
            self.shadertoy.render(time=time)
        w, h = self.size

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
