from sprites.items.item import Item
from sprites.items.piggybank import PiggyBank

SCORE_DESTROY_PIGGYBANK = 100
SCORE_HURT_SKULLSPRITE = 50


class Hammer(Item):
    def on_use_with(self, b, args):
        from sprites.characters.skull import Skull

        if isinstance(b, PiggyBank):
            if b.fade_destroy():
                args.state.play_sound('piggybank', 'destroy')
                args.state.score += SCORE_DESTROY_PIGGYBANK
            return

        if isinstance(b, Skull):
            b.hurt(40)
            args.state.score += SCORE_HURT_SKULLSPRITE
            return

        args.state.noaction(args.player)

    def copy(self):
        """ Copy item """
        return Hammer(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
