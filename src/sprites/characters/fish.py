import random

import arcade

from sprites.characters.character import Character

MOVE_SPEED_X = 7
MOVE_SPEED_Y_FROM = -3
MOVE_SPEED_Y_TO = 3


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
        self.river_from = None
        self.river_to = None
        self.move_y = 0

        self.randomize_move_y()

    def update(
            self,
            delta_time,
            args
    ):

        from constants.layers import LAYER_RIVER

        if self.river_from is None:
            river_parts = arcade.check_for_collision_with_list(self, args.scene[LAYER_RIVER])

            # FIXME: This seems to be switched in this arcade version
            self.river_from = (river_parts[0].center_y - river_parts[0].height / 2) + (self.height * 2)
            self.river_to = (river_parts[0].center_y + river_parts[0].height / 2) - (self.height * 2)

        self.center_x -= MOVE_SPEED_X

        if self.right <= 0:
            self.right = args.tilemap.width + abs(self.right)
            self.randomize_move_y()

        center_y = self.center_y + self.move_y

        if center_y >= self.river_to:
            center_y = self.river_to
            self.randomize_move_y()
            self.move_y = abs(self.move_y) * -1

        if center_y <= self.river_from:
            center_y = self.river_from
            self.move_y *= -1
            self.randomize_move_y()
            self.move_y = abs(self.move_y)

        self.center_y = center_y

    def randomize_move_y(self):
        self.move_y = random.uniform(MOVE_SPEED_Y_FROM, MOVE_SPEED_Y_TO)
