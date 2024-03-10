from sprites.items.item import Item


class RedHerring(Item):
    def on_use(self, b, state=None, handlers=None):
        state.beep()


class Feather(RedHerring):
    pass


class Vase(RedHerring):
    pass
