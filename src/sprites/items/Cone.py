from sprites.items.item import Item
from utils.callbackhandler import CallbackHandler


class Cone(Item):
    def on_use(self, b, state=None, handlers: CallbackHandler | None = None):
        state.beep()
