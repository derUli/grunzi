""" Wall sprite """
from sprites.wall import Wall


class Door(Wall):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='door.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        # For unlocking just set this on true
        self.walkable = False
