import logging

import arcade
import pyglet

from constants.settings import UNLIMITED_FRAMERATE
from utils.text import label_value

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Grunzi"

UPDATE_RATE = 1 / 72


class GameWindow(arcade.Window):
    """
    Main application class.
    """

    def __init__(
            self,
            window: bool = False,
            width: int = SCREEN_WIDTH,
            height: int = SCREEN_HEIGHT,
            update_rate: float = UPDATE_RATE,
            draw_rate: float = UNLIMITED_FRAMERATE,
            vsync: bool = False,
            borderless: bool = False,
            antialiasing: bool = True,
            samples: int = 0,
    ):
        default_screen = pyglet.canvas.get_display().get_default_screen()
        native_mode = default_screen.get_mode()
        self.monitor_refresh_rate = native_mode.rate

        logging.info(label_value('Monitor refresh rate', self.monitor_refresh_rate))

        native_resolution = (native_mode.width, native_mode.height)
        style = pyglet.window.Window.WINDOW_STYLE_DEFAULT
        self.is_native = native_resolution == (width, height)

        if borderless:
            style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS

        logging.debug('Refresh rate ', draw_rate)

        draw_rate = 1 / draw_rate

        self.initial_draw_rate = draw_rate

        # Call the parent class and set up the window
        super().__init__(
            width=width,
            height=height,
            title=SCREEN_TITLE,
            fullscreen=self.is_native,
            update_rate=update_rate,
            draw_rate=draw_rate,
            center_window=True,
            style=style,
            vsync=vsync,
            gc_mode='context_gc',
            antialiasing=antialiasing,
            samples=samples
        )

        self.change_screen_mode(not window)
        self._draw_rate = draw_rate
        self.set_vsync(vsync)
        self.controller_manager = None
        self.controllers = []

    def setup(self) -> None:
        """ Setup the game window"""

        # Enable timings for FPS measurements
        if not arcade.timings_enabled():
            arcade.enable_timings()

        # Init controllers if enabled
        self.init_controllers()

    def change_screen_mode(self, fullscreen: bool = True) -> None:
        """
        Change the screen mode

        @param fullscreen: Is Fullscreen
        """

        if self.is_native:
            return
        screen = pyglet.canvas.get_display().get_default_screen()
        mode = screen.get_closest_mode(self.width, self.height)

        return super().set_fullscreen(fullscreen=fullscreen, screen=screen, mode=mode)

    def init_controllers(self) -> None:
        """ Initialize the connected controllers """

        try:
            self.controller_manager = pyglet.input.ControllerManager()
            for controller in self.controller_manager.get_controllers():
                logging.info(f'Controller: {controller.device.manufacturer} {controller.device.name}')
                controller.open(self)
                self.controllers.append(controller)
        except FileNotFoundError as e:
            logging.error(e)
            self.controllers = []

        if not any(self.controllers):
            logging.info(f"No controllers detected")

    def set_vsync(self, vsync):
        super().set_vsync(vsync)

        if vsync:
            self.set_draw_rate(1 / self.monitor_refresh_rate)
        else:
            self.set_draw_rate(self.initial_draw_rate)
