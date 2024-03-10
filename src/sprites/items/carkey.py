import logging
from typing import Optional

import PIL
import arcade

from sprites.items.item import Item, Jeep
from sprites.sprite import Sprite
from utils.callbackhandler import CallbackHandler


class CarKey(Item):
    def on_use(self, b, state=None, handlers: CallbackHandler|None=None):
        if isinstance(b, Jeep):
            state.play_sound('car', 'start')
            handlers.on_complete()
            return

        state.beep()
