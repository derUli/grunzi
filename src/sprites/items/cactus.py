import logging
from typing import Optional

import arcade
import pyglet

from sprites.characters.character import Character
from sprites.sprite import Sprite
from utils.positionalsound import PositionalSound
from utils.scene import get_layer

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
        self.check_initialized = False

        super().__init__(
            filename=filename,
            image_x=image_x,
            image_y=image_y,
        )

    def update(
            self,
            delta_time,
            args
    ):
        if not self.check_initialized:
            self.check_initialized = True
            pyglet.clock.schedule_interval_soft(self.check_npcs, 1 / 4, args)

        if arcade.check_for_collision(self, args.player):
            args.player.hurt(HURT)

            # TODO: other sound effect
            #audio = args.state.play_sound('electric', 'push')
            #sound = PositionalSound(args.player, self, audio, args.state)
            #sound.update()
            # sound.play()

            move = FORCE_MOVE
            if args.player.center_x < self.center_x:
                move *= -1

            args.physics_engine.apply_force(args.player, (move, 0))

    def check_npcs(self, dt, args):

        from constants.layers import LAYER_NPC

        collisions = arcade.check_for_collision_with_list(
            self,
            get_layer(LAYER_NPC, args.scene)
        )

        for sprite in collisions:
            if isinstance(sprite, Character):
                logging.info(f"Cactus hurt {str(sprite)}")
                sprite.hurt(HURT)

                audio = args.state.play_sound('electric', 'push')
                sound = PositionalSound(sprite, self, audio, args.state)
                sound.update()
                sound.play()
