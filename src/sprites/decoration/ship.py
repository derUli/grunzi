from sprites.sprite import Sprite, AbstractAnimatedSprite

MOVE_X = 0.5


class Ship(Sprite):
    def update(
            self,
            delta_time,
            args
    ):
        self.center_x -= MOVE_X

        if self.right < 0:
            self.remove_from_sprite_lists()


class Steam(AbstractAnimatedSprite):

    def update(
            self,
            delta_time,
            args
    ):
        self.center_x -= MOVE_X

        if self.right < 0:
            self.remove_from_sprite_lists()
