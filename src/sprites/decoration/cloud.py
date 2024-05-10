from sprites.sprite import Sprite

MOVE_SPEED = 0.25


class Cloud(Sprite):
    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        w, h = map_size

        self.center_x -= MOVE_SPEED

        if self.right < 0:
            self.right = w
