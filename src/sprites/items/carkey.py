from sprites.items.item import Item
from sprites.items.jeep import Jeep
from utils.callbackhandler import CallbackHandler


class CarKey(Item):
    def on_use_with(self, b, args):
        if isinstance(b, Jeep):
            args.state.play_sound('car', 'start')
            args.callbacks.on_complete()
            return

        args.state.noaction()

    def copy(self):
        """ Copy item """
        return CarKey(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
