from sprites.sprite import Sprite

CAR_SPEED = 10


class Car(Sprite):
    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        self.center_x += CAR_SPEED

        w, h = map_size
        if self.left > w:
            self.right = 0
