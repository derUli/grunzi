from constants.collisions import COLLISION_CAR, COLLISION_ENEMY, COLLISION_PLAYER, COLLISION_CHICKEN
from sprites.sprite import Sprite

MOVE_SPEED = 0.5



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
            self.left = w + 1
