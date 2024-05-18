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
            scale=1.0
    ):
        self.check_initialized = False
        self.enabled = POWER_ON

        super().__init__(
            filename=filename,
            image_x=image_x,
            image_y=image_y,
            scale=scale
        )

    def update(
            self,
            delta_time,
            args
    ):
        if not self.check_initialized:
            self.check_initialized = True
            pyglet.clock.schedule_interval_soft(self.check_cone, 1 / 3, args.scene)

        if not self.sound:
            audio = args.state.play_sound('electric', 'on', loop=True)
            self.sound = PositionalSound(args.player, self, audio, args.state)
            self.sound.play()

        if not self.enabled:
            alpha = self.alpha - ALPHA_SPEED

            if alpha < 0:
                alpha = 0

            self.alpha = alpha

            if self.alpha == 0:
                self.sound.pause()

            return

        self.sound.play()
        self.sound.update()

        alpha = self.alpha + ALPHA_SPEED

        if alpha > 255:
            alpha = 255

        self.alpha = alpha

        if arcade.check_for_collision(self, args.player):
            audio = args.state.play_sound('electric', 'push')
            sound = PositionalSound(args.player, self, audio, args.state)
            sound.update()
            sound.play()

            args.player.hurt(HURT_PLAYER)
            args.physics_engine.apply_force(args.player, (FORCE_MOVE, 0))

    def check_cone(self, dt, scene):

        from constants.layers import LAYER_ELECTRIC_SWITCH

        for switch in scene[LAYER_ELECTRIC_SWITCH]:

            if not switch.enabled:
                self.enabled = POWER_ON
                return

            self.enabled = POWER_OFF
