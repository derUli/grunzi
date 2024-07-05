""" Postprocessing effect base class  """
import logging

from arcade import SpriteList

from state.argscontainer import ArgsContainer


class Effect:
    """ Postprocessing effect base class  """

    def __init__(self):
        """ Constructor """

        self.spritelist = SpriteList(lazy=True, use_spatial_hash=True)

    def setup(self, args):
        """ Setup effect """

        logging.error('Postprocessing: setup() method not implemented')
        return self

    def update(self, delta_time: float, args: ArgsContainer) -> None:
        """ Update effect"""

        logging.error('Postprocessing: update() method not implemented')

    def draw(self) -> None:
        """ Draw effect"""
        if not self.should_draw:
            return

        self.spritelist.draw()

    @property
    def should_draw(self):
        for sprite in self.spritelist:
            if sprite.alpha >= 1:
                return True

        return False
