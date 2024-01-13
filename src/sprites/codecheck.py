""" Wall sprite """
from sprites.codenumber import CodeNumber
from sprites.sprite import Sprite
from state.level import LAYER_ITEMS, LAYER_STATIC_OBJECTS

TASK_ID = 'find_code'
NEXT_TASK_ID = 'blast'


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
        self.code_valid = False

    def draw(self, screen, x, y):
        """ Not visible """
        return

    def ai(self, level):
        """ Generate number code, Check number code """
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

                if self.code_valid:
                    item.attributes['locked'] = True

        self.code_valid = digits == self.code

        # Purge lasers on enter code
        if self.code_valid:
            z = LAYER_STATIC_OBJECTS
            y = self.y - 1
            x_from = self.x - 5
            x_to = self.x + 1
            for x in range(x_from, x_to):
                if not level.layers[z][y][x]:
                    continue
                level.layers[z][y][x].start_fade()

    def update_state(self, state):
        if self.code_valid:
            if state.task == TASK_ID:
                state.update_task(NEXT_TASK_ID)
            return

        state.update_task(TASK_ID)
