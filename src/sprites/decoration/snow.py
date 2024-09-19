import random

import pyglet
from arcade import SpriteCircle, Color

from sprites.sprite import Sprite

MOVE_X = -1.0

SNOW_COLORS = [
    (255, 255, 255, 255),
    (236, 255, 253, 255),
    (208, 236, 235, 255),
    (160, 230, 236, 255),
    (148, 242, 244, 255)
]


class Snow(SpriteCircle, Sprite):

    def __init__(self, radius: int, color: Color, soft: bool = True):
        super().__init__(radius, color, soft)

    def setup_snow(self, args):
        pyglet.clock.schedule_interval_soft(self.update_snow, 1/72, args)

    def update_snow(self, delta_time, args):
        from constants.layers import LAYER_SNOW

        for snow in args.scene[LAYER_SNOW]:
            snow.center_y += MOVE_X

            if snow.bottom < 0:
                snow.center_x = random.randint(0, args.tilemap.width)
                snow.bottom = random.randint(args.tilemap.height, args.tilemap.height + 10)

    def cleanup(self):
        pyglet.clock.unschedule(self.update_snow)
