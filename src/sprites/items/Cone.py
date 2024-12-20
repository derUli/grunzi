from sprites.items.item import Item


class Cone(Item):
    def on_use_with(self, b, args):
        args.state.noaction(args.player)

    def copy(self):
        """ Copy item """
        return Cone(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
