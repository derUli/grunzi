from sprites.items.item import Item, Fence


class Plier(Item):
    def on_use(self, b, state):
        if isinstance(b, Fence):
            b.remove_from_sprite_lists()
            state.sounds['tools']['plier'].play()
            return

        state.beep()
