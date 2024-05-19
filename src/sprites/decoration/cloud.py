from sprites.sprite import Sprite

MOVE_SPEED = 0.25


class Cloud(Sprite):
    def update(
            self,
            delta_time,
            args
    ):
        w, h = args.map_size

        self.center_x -= MOVE_SPEED

        if self.right <= 0:
            self.right = w - abs(self.right)
