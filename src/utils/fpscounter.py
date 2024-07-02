""" FPS counter """

import time

import arcade

from constants.fonts import FONT_MONOTYPE
from utils.text import create_text, MEDIUM_FONT_SIZE, MARGIN

FPS_UPDATE_INTERVAL = 1


class FPSCounter:
    """ FPS counter class """

    def __init__(self):
        """  Constructor """

        self.current_fps = -1
        self.last_fps_update = time.time()
        self.fps_text = {}

    def reset(self) -> None:
        """ Reset fps counter """

        self.current_fps = -1
        self.fps_text = None

    def update(self, fps: float) -> None:
        """
        Update fps counter

        @param fps: Current fps
        """
        self.current_fps = int(fps)

    def draw(self, size: tuple) -> None:
        """
        Draw fps counter

        @param size: Size of the screen
        """

        if self.current_fps == -1:
            return

        fps = str(self.current_fps)

        fps_text = create_text(
            fps,
            color=arcade.csscolor.LIME_GREEN,
            font_name=FONT_MONOTYPE,
            font_size=MEDIUM_FONT_SIZE,
            bold=True
        )

        w, h = size

        fps_text.x = w - MARGIN - fps_text.content_width
        fps_text.y = h - fps_text.content_height

        fps_text.draw()
