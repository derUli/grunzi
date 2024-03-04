from sprites.sprite import Sprite

CAR_SPEED = 1

class Car(Sprite):
    def update(self, player=None, scene=None, physics_engine=None, state=None, delta_time=None, tilemap=None):
        print('update')
        self.center_x += CAR_SPEED

