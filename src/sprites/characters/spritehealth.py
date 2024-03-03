import logging

HEALTH_FULL = 100.0
HEALTH_EMPTY = 0.0


class SpriteHealth:

    def __init__(self):
        self.health = HEALTH_FULL
        self._died = False

    def _dead(self):
        if self.health < HEALTH_EMPTY:
            self.health = HEALTH_EMPTY

        return self.health <= HEALTH_EMPTY

    def hurt(self, damage):
        self.health -= damage

        return self.dead

    def on_die(self):
        logging.info(f"{self.__class__} is dead")

    @property
    def dead(self):
        if self._died:
            return True

        self._died = self._dead()
        if self._died:
            self.on_die()

            return self._died
