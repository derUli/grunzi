import logging

from sprites.sprite import Sprite


class Item:
    def on_use(self, b):
        logging.info(f"Use item {self} with {b}")

    def copy(self):
        logging.debug('Copy not implemented')
        return self


class Useable:
    pass


class Fence(Sprite, Useable):
    pass
