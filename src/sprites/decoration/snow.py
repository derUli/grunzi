import random

from arcade import SpriteCircle, Color

from sprites.sprite import Sprite

MOVE_X = 1

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

    def update(
            self,
            delta_time,
            args
    ):
        self.top -= MOVE_X

        if self.top > args.tilemap.height:
            self.top = random.randint(0, 10) * - 1
            self.left = random.randint(0, args.tilemap.width)
