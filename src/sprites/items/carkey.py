from sprites.items.item import Item, Jeep
from utils.callbackhandler import CallbackHandler


class CarKey(Item):
    def on_use(self, b, state=None, handlers: CallbackHandler | None = None):
        if isinstance(b, Jeep):
            state.play_sound('car', 'start')
            handlers.on_complete()
            return

        state.beep()
