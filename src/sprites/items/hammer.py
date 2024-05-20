from sprites.items.item import Item
from sprites.items.piggybank import PiggyBank

SCORE_DESTROY_PIGGYBANK = 100
SCORE_HURT_SKULLSPRITE = 50


class Hammer(Item):
    def on_use_with(self, b, state=None, handlers=None):
        from sprites.characters.skull import Skull

        if isinstance(b, PiggyBank):
            if b.fade_destroy():
                state.play_sound('piggybank', 'destroy')
                state.score += SCORE_DESTROY_PIGGYBANK
            return

        if isinstance(b, Skull):
            b.hurt(40)
            state.score += SCORE_HURT_SKULLSPRITE
            return

        state.beep()

    def copy(self):
        """ Copy item """
        return Hammer(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
