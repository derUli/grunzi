from sprites.sprite import Sprite

MOVE_SPEED = 5


class River(Sprite):
    def update(
            self,
            delta_time,
            args
    ):
        w, h = args.map_size
        self.alpha = 200
        self.center_x -= MOVE_SPEED

        if self.right <= 0:
            self.right = w - abs(self.right)