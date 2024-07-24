from sprites.sprite import Sprite

MOVE_X = 1


class Ship(Sprite):
    def update(
            self,
            delta_time,
            args
    ):
        self.center_x -= MOVE_X

        if self.right < 0:
            self.remove_from_sprite_lists()
