""" Postprocessing effect base class  """
import logging

from arcade import SpriteList

from state.argscontainer import ArgsContainer


class Effect:
    """ Postprocessing effect base class  """

    def __init__(self, enabled: bool = True):
        """ Constructor """

        self.spritelist = SpriteList(lazy=True, use_spatial_hash=False)
        self.enabled = enabled

    def setup(self, args: ArgsContainer):
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
        if not self.enabled:
            return False

        for sprite in self.spritelist:
            if sprite.alpha >= 1:
                return True

        return False

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        self._enabled = enabled

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = True

    def toggle(self):
        self.enabled = not self.enabled
