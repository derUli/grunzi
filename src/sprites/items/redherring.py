
from sprites.items.item import Item


class RedHerring(Item):
    def on_use(self, b, state):
        state.beep()
