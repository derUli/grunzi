""" Guitar sprite """
from sprites.coin import Coin
from sprites.sprite import Sprite
import random

class Telescope(Sprite):
    """ Guitar sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'telescope.png')
        self.sound = None
        code = [1, 2, 3, 4]
        random.shuffle(code)

        self.attributes = {
            'code': code
        }

    def handle_interact(self, element):
        if element and element.state:
            element.state.say(_('[Insert Coin]'))

    def handle_interact_item(self, element):
        # Activate the telescope with a coin
        if not element:
            return

        if isinstance(element.state.inventory, Coin):
            element.state.say(_('Not implemented yet'))
            element.state.use_item = False
            # element.state.inventory = None
