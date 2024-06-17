from typing import Optional

import arcade

from sprites.sprite import Sprite
from utils.positionalsound import PositionalSound

FORCE_MOVE = 5000
HURT = 1


class Cactus(Sprite):
    def __init__(
            self,
            filename: Optional[str] = None,
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

        super().__init__(
            filename=filename,
            image_x=image_x,
            image_y=image_y,
        )

        self.measurements = []

    def update(
            self,
            delta_time,
            args
    ):

        if arcade.check_for_collision(self, args.player):
            args.player.hurt(HURT)

            audio = args.state.play_sound('cactus')
            sound = PositionalSound(args.player, self, audio, args.state)
            sound.update(True)
            sound.play()

            move = FORCE_MOVE
            if args.player.center_x < self.center_x:
                move *= -1

            args.physics_engine.apply_force(args.player, (move, 0))
