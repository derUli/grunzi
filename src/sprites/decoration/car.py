import logging

import arcade
import pyglet

from constants.collisions import COLLISION_CAR, COLLISION_ENEMY, COLLISION_PLAYER, COLLISION_CHICKEN
from sprites.sprite import Sprite
from state.argscontainer import ArgsContainer

# MOV_
FORCE_MOVE = 4000

# Hurt NPCs on collide with car
HURT = 34


class Car:
    def remove_food(self, delta_time, args):
        from constants.layers import LAYER_FOOD
        try:
            food = args.scene[LAYER_FOOD]
        except KeyError:
            return

        food = filter(lambda x: arcade.get_distance_between_sprites(self, x) <= 200, food)

        print(arcade.get_distance_between_sprites(self, args.player))

        for meal in food:
            logging.info('Car collided with food')
            meal.remove_from_sprite_lists()


    def setup_handlers(self, args):
        args.physics_engine.add_collision_handler(COLLISION_CAR, COLLISION_ENEMY, post_handler=self.on_hit)
        args.physics_engine.add_collision_handler(COLLISION_CAR, COLLISION_PLAYER, post_handler=self.on_hit)
        args.physics_engine.add_collision_handler(COLLISION_CAR, COLLISION_CHICKEN, post_handler=self.on_hit)

        pyglet.clock.schedule_interval_soft(self.remove_food, 2, args=args)

    def on_hit(self, _car_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """

        _hit_sprite.hurt(HURT)


class CarLeft(Sprite, Car):
    def setup(self, args):
        self.setup_handlers(args)

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ) -> None:
        w, h = args.map_size

        args.physics_engine.apply_force(self, (-FORCE_MOVE, 0))

        if self.right < 0:
            args.physics_engine.set_position(self, (w - self.width / 2, self.center_y))


    def cleanup(self):
        pyglet.clock.unschedule(self.remove_food)

class CarRight(Sprite, Car):
    def setup(self, args):
        self.setup_handlers(args)

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ) -> None:
        args.physics_engine.apply_force(self, (FORCE_MOVE, 0))

        w, h = args.map_size
        if self.right > w:
            args.physics_engine.set_position(self, (0 - self.width / 2, self.center_y))

    def cleanup(self):
        pyglet.clock.unschedule(self.remove_food)
