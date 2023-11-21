""" Wall sprite """
from sprites.sprite import Sprite
from sprites.codenumber import CodeNumber
from state.level import LAYER_ITEMS

class CodeCheck(Sprite):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.code = None
        self.x = None
        self.y = None
        self.z = None
    def draw(self, screen, x, y):
        return

    def ai(self, level):
        if not self.code:
            z, y, x = level.search_by_id('telescope')
            telescope = level.layers[z][y][x]
            self.code = telescope.attributes['code']

            self.z, self.y, self.x = level.search_sprite(self)

        digits = []

        for x in range(self.x - 4, self.x):
            item = level.layers[LAYER_ITEMS][self.y][x]
            if isinstance(item, CodeNumber):
                digits.append(item.attributes['digit'])

        if digits == self.code:
            print('TODO: Handle correct code')
