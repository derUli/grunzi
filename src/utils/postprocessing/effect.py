import logging
from arcade import SpriteList

class Effect:
    def __init__(self):
        self.spritelist = SpriteList(lazy=True, use_spatial_hash=True)

    def setup(self, args):
        logging.error('Postprocessing: setup() method not implemented')
        return self

    def update(self, delta_time, args):
        logging.error('Postprocessing: update() method not implemented')

    def draw(self):
        self.spritelist.draw()