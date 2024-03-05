from sprites.sprite import Sprite

CAR_SPEED = 10
FORCE_MOVE = 4000

class CarRight(Sprite):
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


class CarLeft(Sprite):
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
