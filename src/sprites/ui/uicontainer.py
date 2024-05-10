import arcade

from constants.fonts import FONT_MONOTYPE
from sprites.ui.inventorycontainer import InventoryContainer
from utils.text import create_text

r, g, b, a = arcade.csscolor.HOTPINK
BACKGROUND_COLOR = (r, g, b, 10)
HEIGHT = 84
MARGIN = 10
FILL_COUNT = 5
FILL_CHAR = '0'

class UIContainer:
    def __init__(self):
        """ Constructor """
        self.inventory = None
        self.state = None
        self.size = None
        self.rendered_score_text = {}

    def setup(self, state, size):
        """ Setup UI """

        self.state = state
        self.size = size

        self.inventory = InventoryContainer()
        self.inventory.setup(state=state, size=size)

        self.rendered_score_text = {}

    def draw(self):
        """ Draw UI """
        # self.background.draw()

        if str(self.state.score) not in self.rendered_score_text:
            formatted_score = str(self.state.score).rjust(FILL_COUNT, FILL_CHAR)
            text = create_text(
                _("Score") + ":\n" + str(formatted_score),
                multiline=True,
                width=100,
                color=arcade.csscolor.HOTPINK,
                align='center',
                bold=True,
                font_name=FONT_MONOTYPE,
            )
            w, h = self.size
            text.y = (h - MARGIN - text.content_height)

            self.rendered_score_text[str(self.state.score)] = text

        self.rendered_score_text[str(self.state.score)].draw()
        self.inventory.draw()
