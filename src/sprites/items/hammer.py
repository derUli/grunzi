from sprites.items.item import Item, PiggyBank


class Hammer(Item):
    def on_use(self, b, state=None, handlers=None):
        from sprites.characters.ferret import Ferret
        from sprites.characters.skullsprite import SkullSprite

        if isinstance(b, PiggyBank):
            b.fade_destroy()
            state.play_sound('piggybank', 'destroy')
            return

        if isinstance(b, SkullSprite):
            b.hurt(40)
            return

        if isinstance(b, Ferret):
            b.hurt(80)
            return

        state.beep()
