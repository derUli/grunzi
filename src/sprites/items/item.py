import logging

import arcade

from sprites.sprite import Sprite


class Item:
    def on_use(self, b):
        logging.info(f"Use item {self} with {b}")


class Useable:
    pass


class Fence(Sprite, Useable):
    pass
