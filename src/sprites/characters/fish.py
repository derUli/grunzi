import random

import arcade
from arcade import FACE_RIGHT, FACE_LEFT

from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL, HEALTHBAR_FREN_COLOR
from sprites.items.item import Useable
from utils.positional_sound import PositionalSound


MOVE_SPEED = 7

class Fish(Character):
    def __init__(
            self,
            filename: str | None = None,
            image_x=0,
            image_y=0,
            image_width=None,
            image_height=None,
            flipped_horizontally=False,
            flipped_vertically=False,
            flipped_diagonally=False,
            hit_box_algorithm=None,
            hit_box_detail=None,
            scale=1.0,
            center_x=None,
            center_y=None
    ):
        super().__init__(filename, center_x=center_x, center_y=center_y)

    def update(
            self,
            delta_time,
            args
    ):
        return
        self.center_x -= MOVE_SPEED


        if self.right <= 0:
            self.right = args.tilemap.width + abs(self.right)

        # self.angle += 1