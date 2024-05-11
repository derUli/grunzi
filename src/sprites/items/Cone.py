from sprites.items.item import Item
from utils.callbackhandler import CallbackHandler


class Cone(Item):
    def on_use(self, b, state=None, handlers: CallbackHandler | None = None):
        state.beep()

    def copy(self):
        """ Copy item """
        return Cone(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
