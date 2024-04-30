from sprites.items.item import Item, PiggyBank


class Chainsaw(Item):
    def on_use(self, b, state=None, handlers=None):
        from sprites.characters.ferret import Ferret
        from sprites.characters.skullsprite import SkullSprite

        if isinstance(b, PiggyBank):
            b.fade_destroy()
            # TODO: Chainsaw sound
            state.play_sound('piggybank', 'destroy')
            return

        if isinstance(b, SkullSprite):
            b.hurt(50)
            return
        if isinstance(b, Ferret):
            b.hurt(100)
            return

        state.beep()
