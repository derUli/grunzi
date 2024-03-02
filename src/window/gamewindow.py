import logging

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
            update_rate=UPDATE_RATE,
            controller=True
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

        self.controller = controller

        self.debug = debug
        self.show_fps = debug
        self.controllers = []

    def setup(self):
        # Enable timings for FPS measurements
        if not arcade.timings_enabled():
            arcade.enable_timings()

        # Init controllers if enabled
        if self.controller:
            self.init_controllers()

    def set_fullscreen(self, fullscreen=True):
        screen = pyglet.canvas.get_display().get_default_screen()
        mode = screen.get_closest_mode(self.width, self.height)

        return super().set_fullscreen(fullscreen=fullscreen, screen=screen, mode=mode)

    def size(self):
        return self.width, self.height

    def init_controllers(self):
        if self.controllers:
            return

        try:
            self.controllers = arcade.get_game_controllers()
        except FileNotFoundError as e:
            logging.error(e)
            self.controllers = []
        if not any(self.controllers):
            logging.info(f"Controller: No controllers detected")

        for controller in self.controllers:
            logging.info(f'Controller: Init {controller.device.name}')
            controller.open(self)