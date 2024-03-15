from sprites.items.item import Item, Jeep
from utils.callbackhandler import CallbackHandler


class CarKey(Item):
    def on_use(self, b, state=None, handlers: CallbackHandler | None = None):
        if isinstance(b, Jeep):
            sound = state.play_sound('car', 'start')
            handlers.on_complete(wait_for_sound=sound)
            return

        state.beep()
