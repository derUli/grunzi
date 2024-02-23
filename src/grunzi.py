"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import os

import arcade
import pyglet

from state.viewstate import ViewState
from views.gameview import GameView

SCREEN_TITLE = "Grunzi"

ROOT_DIR = os.path.dirname(__file__)

SCREEN = pyglet.canvas.get_display().get_default_screen()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Constants used to scale our sprites from their original size
TILE_SCALING = 1.0

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10


class GameWindow(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE, fullscreen=True, vsync=True)


def main():
    """Main function"""
    window = GameWindow()
    state = ViewState(ROOT_DIR)
    view = GameView(window, state)
    view.setup()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
