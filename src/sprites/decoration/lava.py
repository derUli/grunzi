import arcade
import pyglet.clock

from sprites.sprite import AbstractAnimatedSprite


class Lava(AbstractAnimatedSprite):

    def setup(self, args):
        pyglet.clock.schedule_interval_soft(self.check_for_collision, 1 / 6, args)

    def check_for_collision(self, delta_time, args):
        # Hurt player
        if arcade.check_for_collision(self, args.player):
            args.player.hurt(10)
            return

    def cleanup(self):
        pyglet.clock.unschedule(self.check_for_collision)
