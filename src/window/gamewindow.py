import arcade
import pyglet

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Grunzi"

UPDATE_RATE = 1 / 60
DRAW_RATE = 1 / 60


class GameWindow(arcade.Window):
    """
    Main application class.
    """

    def __init__(
            self,
            window=False,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            debug=False,
            update_rate=UPDATE_RATE
    ):
        # Call the parent class and set up the window
        super().__init__(
            width=width,
            height=height,
            title=SCREEN_TITLE,
            fullscreen=False,
            vsync=True,
            update_rate=update_rate
        )

        self.set_fullscreen(not window)

        self.update_rate = update_rate
        self.draw_rate = update_rate

        self.debug = debug
        self.show_fps = debug

        # Enable timings for FPS measurements
        if not arcade.timings_enabled():
            arcade.enable_timings()

    def set_fullscreen(self, fullscreen=True):
        screen = pyglet.canvas.get_display().get_default_screen()
        mode = screen.get_closest_mode(self.width, self.height)

        return super().set_fullscreen(fullscreen=fullscreen, screen=screen, mode=mode)

    def size(self):
        return self.width, self.height
