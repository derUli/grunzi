from sprites.items.item import Item


class RedHerring(Item):
    def on_use_with(self, b, state=None, handlers=None):
        state.beep()


class Feather(RedHerring):

    def copy(self):
        """ Copy item """
        return Feather(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )


class Vase(RedHerring):

    def copy(self):
        """ Copy item """
        return Vase(
            filename=self.filename,
            center_x=self.center_x,
            center_y=self.center_y
        )
