import logging

from sprites.items.item import Item


class Hammer(Item):
    def on_use(self, b, state):
        logging.debug('TODO: implement use hammer')

        state.beep()
