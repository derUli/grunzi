import PIL
import logging
from arcade import FACE_DOWN, FACE_RIGHT, FACE_LEFT

from sprites.items.fence import Fence
from sprites.items.item import Item

SCORE_DESTROY_FENCE = 100


class Lantern(Item):
    def on_equip(self, args):
        logging.info('Equip lantern')

        
    def on_unequip(self, args):
        logging.info('Unequip lantern')

    def copy(self):
        """ Copy item """
        return Lantern(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
