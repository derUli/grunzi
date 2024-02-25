
HEALTH_FULL = 100.0
HEALTH_EMPTY = 0.0

class SpriteHealth:

    def __init__(self):
        self.health = HEALTH_FULL

    def dead(self):
        if self.health < HEALTH_EMPTY:
            self.health = HEALTH_EMPTY

        return self.health <= HEALTH_EMPTY

    def hurt(self, damage):
        self.health -= damage

        return self.dead()