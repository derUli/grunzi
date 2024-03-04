import logging

import arcade


class Item:
    def on_use(self, b):
        logging.info(f"Use item {self} with {b}")


class Useable:
    pass


class Fence(arcade.sprite.Sprite, Useable):
    pass
