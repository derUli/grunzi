""" Wall sprite """
from sprites.sprite import Sprite


class Takeable(Sprite):
    """ Takeable sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        # For unlocking just set this on true
        self.walkable = True

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

    def handle_interact(self, element):
        """ Set walkable on interact """

        element.state.take_item(self)

        self.purge = True
