import logging

import arcade

from constants.collisions import COLLISION_CAR, COLLISION_ENEMY, COLLISION_PLAYER, COLLISION_CHICKEN
from sprites.sprite import Sprite
from state.argscontainer import ArgsContainer

# MOV_
FORCE_MOVE = 4000

# Hurt NPCs on collide with car
HURT = 34


class Car:

    def setup_handlers(self, args):
        args.physics_engine.add_collision_handler(COLLISION_CAR, COLLISION_ENEMY, post_handler=self.on_hit)
        args.physics_engine.add_collision_handler(COLLISION_CAR, COLLISION_PLAYER, post_handler=self.on_hit)
        args.physics_engine.add_collision_handler(COLLISION_CAR, COLLISION_CHICKEN, post_handler=self.on_hit)

    def on_hit(self, _car_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """

        _hit_sprite.hurt(HURT)


    def remove_colliding(self, scene):
        from constants.layers import LAYER_FOOD, LAYER_FEATHER

        self._remove_colliding(scene, LAYER_FOOD)
        self._remove_colliding(scene, LAYER_FEATHER)

    def _remove_colliding(self, scene, layer):

        try:
            food = scene[layer]
        except KeyError:
            return

        food = filter(lambda x: arcade.get_distance_between_sprites(self, x) <= 300, food)
        food = filter(lambda x: arcade.check_for_collision(self, x), food)

        for meal in food:
            logging.info('Car collided with ' + layer)
            meal.remove_from_sprite_lists()


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

        self.remove_colliding(args.scene)


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

        self.remove_colliding(args.scene)