""" Burger sprite class """

from sprites.food import Food

NUTRITIONAL_VALUE = 60

class Burger (Food):
    """ burger sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'burger.png')

        self.nutritional_value = NUTRITIONAL_VALUE
