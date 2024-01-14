""" Apple sprite class """

from sprites.food import Food

NUTRITIONAL_VALUE = 30

class Apple(Food):
    """ Apple sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'apple.png')

        self.nutritional_value = NUTRITIONAL_VALUE