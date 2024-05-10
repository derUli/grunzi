from sprites.items.item import Item, PiggyBank


SCORE_DESTROY_PIGGYBANK = 100
SCORE_HURT_SKULLSPRITE = 50

class Hammer(Item):
    def on_use(self, b, state=None, handlers=None):
        from sprites.characters.skullsprite import SkullSprite

        if isinstance(b, PiggyBank):
            if b.fade_destroy():
                state.play_sound('piggybank', 'destroy')
                state.score += SCORE_DESTROY_PIGGYBANK
            return

        if isinstance(b, SkullSprite):
            b.hurt(40)
            state.score += SCORE_HURT_SKULLSPRITE
            return

        state.beep()
