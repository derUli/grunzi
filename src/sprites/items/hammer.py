from sprites.items.item import Item, PiggyBank


class Hammer(Item):
    def on_use(self, b, state=None, handlers=None):
        from sprites.characters.skullsprite import SkullSprite

        if isinstance(b, PiggyBank):
            if b.fade_destroy():
                state.play_sound('piggybank', 'destroy')
            return

        if isinstance(b, SkullSprite):
            b.hurt(40)
            return

        state.beep()
