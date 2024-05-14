from typing import Optional

import arcade
import pyglet

from sprites.sprite import AbstractAnimatedSprite
from utils.positional_sound import PositionalSound

FORCE_MOVE = 30000
HURT_PLAYER = 5

ALPHA_SPEED = 8.5

POWER_ON = 1
POWER_OFF = 0

class Electric(AbstractAnimatedSprite):
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
        self.enabled = POWER_ON

        super().__init__(
            filename=filename,
            image_x=image_x,
            image_y=image_y,
        )
    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        if not self.check_initialized:
            self.check_initialized = True
            pyglet.clock.schedule_interval_soft(self.check_cone, 1 / 3, scene)



        if not self.sound:
            audio = state.play_sound('electric', 'on', loop=True)
            self.sound = PositionalSound(player, self, audio, state)
            self.sound.play()

        if not self.enabled:
            alpha = self.alpha - ALPHA_SPEED

            if alpha < 0:
                alpha = 0

            self.alpha = alpha

            # TODO: Fade
            if self.alpha == 0:
                self.sound.pause()

            return

        self.sound.play()
        self.sound.update()

        alpha = self.alpha + ALPHA_SPEED

        if alpha > 255:
            alpha = 255

        self.alpha = alpha

        if arcade.check_for_collision(self, player):
            audio = state.play_sound('electric', 'push')
            sound = PositionalSound(player, self, audio, state)
            sound.update()
            sound.play()

            player.hurt(HURT_PLAYER)
            physics_engine.apply_force(player, (FORCE_MOVE, 0))


    def check_cone(self, dt, scene):

        from constants.layers import LAYER_CONES, LAYER_ELECTRIC_SWITCH

        for switch in scene[LAYER_ELECTRIC_SWITCH]:

            if not switch.enabled:
                self.enabled = POWER_ON
                return

            self.enabled = POWER_OFF
