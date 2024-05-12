import arcade

from state.viewstate import ViewState
from utils.text import create_text, MARGIN, EXTRA_LARGE_FONT_SIZE

BAR_HEIGHT = 30
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

        # TODO: Progress bar

    def setup(self, state: ViewState, size: tuple):
        if state.settings.shaders:
            self.shadertoy = state.load_shader(size, 'gameover')

        w, h = size
        self.size = size

        self.onepercent = w / 100

        self.loading_text = create_text(
            _("Loading..."),
            width=w - (MARGIN * 2),
            font_size=EXTRA_LARGE_FONT_SIZE,
            align='left'
        )

        self._percent = 0
        self._display_percentage = 0

        self.loading_text.x = w / 2 - self.loading_text.content_width / 2
        self.loading_text.y = h / 2 - self.loading_text.content_height / 2

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
        if self._percent > self._display_percentage:
            self._display_percentage += PERCENTAGE_SPEED

        elif self._percent < self._display_percentage:
            self._display_percentage -= PERCENTAGE_SPEED

    @property
    def completed(self):
        return self._display_percentage >= 100

    def draw(self, time=None):
        if self.shadertoy:
            self.shadertoy.render(time=time)
        w, h = self.size

        arcade.draw_rectangle_filled(
            w / 2,
            BAR_HEIGHT / 2,
            w,
            BAR_HEIGHT,
            arcade.csscolor.PINK
        )

        bar_width = self._display_percentage * self.onepercent

        arcade.draw_rectangle_filled(
            bar_width / 2,
            BAR_HEIGHT / 2,
            bar_width,
            BAR_HEIGHT,
            arcade.csscolor.HOTPINK
        )

        self.loading_text.draw()
