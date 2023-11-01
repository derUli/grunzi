""" Wall sprite """
import sprites.sprite


class Wall(sprites.sprite.Sprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'wall.jpg')
        self.walkable = False
