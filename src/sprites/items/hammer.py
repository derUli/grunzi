import logging
from typing import Optional

import PIL
import arcade

from sprites.items.item import Item, Fence
from sprites.sprite import Sprite


class Hammer(Item):
    def on_use(self, b, state):
        logging.debug('TODO: implement use hammer')