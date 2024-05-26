import PIL
import logging
from arcade import FACE_DOWN, FACE_RIGHT, FACE_LEFT

from sprites.items.fence import Fence
from sprites.items.item import Item
from utils.lightmanager import LIGHT_LAYER_LANTERN

SCORE_DESTROY_FENCE = 100


class Lantern(Item):

    def on_equip(self, args):
        """
        Toggle light on equip

        @param: ArgsContainer
        
        """
        args.scene.light_manager.enable_layer(LIGHT_LAYER_LANTERN)

    def on_unequip(self, args):
        args.scene.light_manager.disable_layer(LIGHT_LAYER_LANTERN)

    def copy(self):
        """ Copy item """
        return Lantern(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )

    def update(self, delta_time, args):
        args.scene.light_manager.enable_layer(LIGHT_LAYER_LANTERN)
