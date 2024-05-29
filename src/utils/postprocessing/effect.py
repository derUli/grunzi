""" Postprocessing effect base class  """
import logging

from arcade import SpriteList


class Effect:
    """ Postprocessing effect base class  """

    def __init__(self):
        """ Constructor """
        self.spritelist = SpriteList(lazy=True, use_spatial_hash=True)

    def setup(self, args):
        """ Setup effect """
        logging.error('Postprocessing: setup() method not implemented')
        return self

    def update(self, delta_time, args) -> None:
        """ Update effect"""
        logging.error('Postprocessing: update() method not implemented')

    def draw(self) -> None:
        """ Draw effect"""
        self.spritelist.draw()
