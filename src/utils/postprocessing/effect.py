import logging

from arcade import SpriteList


DEFAULT_VALUE = 200

class Effect:
    def __init__(self):
        self.pipeline = []
        self.spritelist = SpriteList(lazy=True, use_spatial_hash=True)

    def setup(self, args):
        logging.error('Postprocessing: setup() method not implemented')

    def update(self, delta_time, args):
        logging.error('Postprocessing: update() method not implemented')

    def draw(self):
        logging.error('Postprocessing: draw() method not implemented')