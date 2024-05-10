from sprites.ui.inventorycontainer import InventoryContainer


class UIContainer:
    def __init__(self):
        """ Constructor """
        self.inventory = None

    def setup(self, state, size):
        """ Setup UI """
        self.inventory = InventoryContainer()
        self.inventory.setup(state=state, size=size)

    def draw(self):
        """ Draw UI """
        self.inventory.draw()