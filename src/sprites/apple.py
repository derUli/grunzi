""" Apple sprite class """
import sprites.sprite


class Apple(sprites.sprite.Sprite):
    """ Apple sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'apple.png')

    def handle_interact(self, element):
        if element and element.state and element.state.health < 100:
            element.state.partial_heal(30)
            self.purge = True
            self.walkable = True
