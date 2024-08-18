import random

from arcade import SpriteCircle
from arcade.types import Color, RGBA255

from constants.layers import LAYER_WALL, LAYER_FIRE
from sprites.sprite import Sprite

MOVE_X = -1

SNOW_COLORS = [
    (255, 255, 255, 255),
    (236, 255, 253, 255),
    (208, 236, 235, 255),
    (160, 230, 236, 255),
    (148, 242, 244, 255)
]

COLLISION_LAYERS = [
    LAYER_WALL,
    LAYER_FIRE
]


class Snow(SpriteCircle, Sprite):

    def __init__(self, radius: int, color: RGBA255, soft: bool = True):
        super().__init__(radius, color, soft)

    def update(
            self,
            delta_time,
            args
    ):
        self.center_y += MOVE_X

        if self.bottom < 0:
            self.center_x = random.randint(0, args.tilemap.width)
            self.bottom = random.randint(args.tilemap.height, args.tilemap.height + 10)
