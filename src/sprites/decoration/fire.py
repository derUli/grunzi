import arcade
import pyglet.clock

from sprites.characters.character import Character
from sprites.sprite import AbstractAnimatedSprite
from state.argscontainer import ArgsContainer
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_SOUND


class Fire(AbstractAnimatedSprite):

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ):
        super().update(delta_time, args)

        if not hasattr(self, 'fx'):
            audio = args.state.play_sound('fire', loop=True)
            self.fx = PositionalSound(
                args.player,
                self,
                audio,
                args.state,
                volume_source=VOLUME_SOURCE_SOUND
            )
            self.fx.update(init=True)
            pyglet.clock.schedule_interval_soft(self.check_for_collision, 1 / 4, args)
            return

        self.fx.update()

    def check_for_collision(self, delta_time, args):
        # Hurt player
        if arcade.check_for_collision(self, args.player):
            args.player.hurt(10)
            return

        from constants.layers import LAYER_NPC

        if not LAYER_NPC in args.scene.name_mapping:
            return

        collisions = arcade.check_for_collision_with_list(self, args.scene[LAYER_NPC])

        for collision in collisions:
            if isinstance(collision, Character):
                collision.hurt(10)
                return
