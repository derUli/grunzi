from sprites.items.item import Item
from sprites.items.valvetarget import ValveTarget


class Valve(Item):
    def on_use_with(self, b, args):

        from constants.layers import LAYER_RIVER

        self.position = b.position

        if isinstance(b, ValveTarget):
            # TODO: Animate

            args.state.play_sound('valve')
            self.turn_right()

            alpha = None

            for water in args.scene[LAYER_RIVER]:
                if alpha is None:
                    alpha = water.alpha - 50

                if alpha <= 0:
                    alpha = 0

                water.alpha = alpha

            for water in args.scene[LAYER_RIVER]:
                water.alpha = alpha

                if alpha <= 0:
                    water.remove_from_sprite_lists()

            return

        # TODO:
        args.state.noaction()

    def copy(self):
        """ Copy item """
        return Valve(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
