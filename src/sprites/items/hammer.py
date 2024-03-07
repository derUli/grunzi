
from sprites.items.item import Item, PiggyBank


class Hammer(Item):
    def on_use(self, b, state):
        if isinstance(b, PiggyBank):
            b.remove_from_sprite_lists()
            state.play_sound('piggybank', 'destroy')
            return

        state.beep()