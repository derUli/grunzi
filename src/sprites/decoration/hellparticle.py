import random

from arcade import SpriteCircle, Color

from sprites.sprite import Sprite

MOVE_X = -1

HELL_PARTICLE_COLORS = [
    (218, 150, 63),
    (33, 212, 37),
    (163, 251, 125)
]


class HellParticle(SpriteCircle, Sprite):

    def __init__(self, radius: int, color: Color, soft: bool = True):
        super().__init__(radius, color, soft)

        self.speed = random.uniform(1, 40)

    def update(
            self,
            delta_time,
            args
    ):
        self.center_x -= self.speed

        if self.right <= 0:
            self.speed = random.uniform(1, 40)
            self.left = args.tilemap.width
            self.center_y = random.randint(0, args.tilemap.height)
