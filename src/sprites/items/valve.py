from sprites.items.item import Item


class Valve(Item):
    def on_use_with(self, b, args):
        # TODO:
        args.state.noaction()

    def copy(self):
        """ Copy item """
        return Valve(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
