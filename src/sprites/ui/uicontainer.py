from sprites.ui.inventorycontainer import InventoryContainer


class UIContainer:
    def __init__(self):
        self.inventory = None

    def setup(self, state, size):
        self.inventory = InventoryContainer()
        self.inventory.setup(state=state, size=size)

    def draw(self):
        self.inventory.draw()