""" FPS counter """

import logging
import time

import arcade
import numpy

from constants.fonts import FONT_MONOTYPE
from constants.layers import LAYER_NPC
from utils.scene import get_layer
from utils.text import create_text, MEDIUM_FONT_SIZE, MARGIN, label_value

FPS_UPDATE_INTERVAL = 1


class FPSCounter:
    def __init__(self):
        """ FPS counter class """
        self.fps = []
        self.current_fps = -1
        self.last_fps_update = 0
        self.fps_text = {}

    def reset(self):
        self.fps = []
        self.current_fps = -1
        self.last_fps_update = 0
        self.fps_text = {}

    def update(self, fps):
        self.fps.append(fps)

        if numpy.max(self.fps) == 0:
            return

        if time.time() > self.last_fps_update + FPS_UPDATE_INTERVAL:
            self.last_fps_update = time.time()
            self.current_fps = int(fps)

    def draw(self, size):

        if self.current_fps == -1:
            return

        fps = str(self.current_fps)

        if fps not in self.fps_text:
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

            self.fps_text[fps] = fps_text

        self.fps_text[fps].draw()