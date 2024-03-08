from sprites.items.item import Item, PiggyBank


class Hammer(Item):
    def on_use(self, b, state):
        if isinstance(b, PiggyBank):
            b.fade_destroy()
            state.play_sound('piggybank', 'destroy')
            return

        state.beep()
