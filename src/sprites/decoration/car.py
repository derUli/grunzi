from sprites.sprite import Sprite

CAR_SPEED = 10
FORCE_MOVE = 4000
HURT = 2


class Car:
    def on_hit(self, _car_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """

        _hit_sprite.hurt(HURT)


class CarRight(Sprite, Car):
    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        physics_engine.apply_force(self, (FORCE_MOVE, 0))

        w, h = map_size
        if self.left > w:
            physics_engine.set_position(self, (0 - self.width, self.center_y))


class CarLeft(Sprite, Car):
    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        physics_engine.apply_force(self, (-FORCE_MOVE, 0))

        w, h = map_size
        if self.right < 0:
            physics_engine.set_position(self, (w, self.center_y))

        physics_engine.add_collision_handler('car', 'enemy', post_handler=self.on_hit)
        physics_engine.add_collision_handler('car', 'player', post_handler=self.on_hit)
