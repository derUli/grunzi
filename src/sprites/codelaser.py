""" CodeLaser sprite """

from constants.direction import DIRECTION_UP, DIRECTION_DOWN
from sprites.fadeable import Fadeable

OFFSET_FROM = -25
OFFSET_TO = 25
MOVE_SPEED = 0.1


class CodeLaser(Fadeable):
    """ Backdrop sprite """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.walkable = False
        self.direction = DIRECTION_DOWN
        self.offset_y = 0
        self.cached = {}

    def draw(self, screen, x, y):
        """ draw sprite """
        x, y = self.calculate_pos(x, y)

        y += self.offset_y

        screen.blit(self.sprite, (x, y))

        if self.direction == DIRECTION_DOWN:
            self.offset_y += MOVE_SPEED
            if self.offset_y > OFFSET_TO:
                self.direction = DIRECTION_UP
        else:
            self.offset_y -= MOVE_SPEED

            if self.offset_y < OFFSET_FROM:
                self.direction = DIRECTION_DOWN
