import arcade
import pyglet.clock

from sprites.characters.character import Character
from sprites.sprite import AbstractAnimatedSprite
from state.argscontainer import ArgsContainer

ALPHA_MAX = 255
ALPHA_SPEED = 3
SCALE_SPEED_GROW = 0.05
SCALE_SPEED_SHRINK = 0.1
SCALE_MAX = 20
SCALE_MIN = 1


class Portal(AbstractAnimatedSprite):

    def setup(self, args):
        self.alpha = 0
        self.collides = False

        pyglet.clock.schedule_interval_soft(self.check_collision, 1 / 4, args)

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ):
        from constants.layers import LAYER_SWITCH

        for switch in args.scene[LAYER_SWITCH]:
            if switch.enabled == 0:
                return

        if self.alpha < ALPHA_MAX:
            alpha = self.alpha + ALPHA_SPEED

            if alpha > ALPHA_MAX:
                alpha = ALPHA_MAX

            self.alpha = alpha

        if self.collides:
            if self.scale < SCALE_MAX:
                self.scale += SCALE_SPEED_GROW
            else:
                args.callbacks.on_complete()
        else:
            if self.scale > SCALE_MIN:
                self.scale -= SCALE_SPEED_SHRINK

    def check_collision(self, delta_time, args):
        if self.alpha <= 0:
            return

        from constants.layers import LAYER_NPC

        npcs = arcade.check_for_collision_with_list(self, args.scene[LAYER_NPC])
        for npc in npcs:
            if isinstance(npc, Character):
                npc.health = 0

        self.collides = arcade.check_for_collision(self, args.player)


    def unschedule(self):
        pyglet.clock.unschedule(self.check_collision)