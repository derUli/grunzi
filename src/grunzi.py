"""
Platformer Template

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.template_platformer
"""
import gettext
import locale
import os

import arcade
import pyglet.image

from state.viewstate import ViewState
from views.mainmenuview import MainMenuView

SCREEN_TITLE = "Grunzi"

ROOT_DIR = os.path.dirname(__file__)

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

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

    # Set locale
    locale_path = os.path.join(ROOT_DIR, 'data', 'locale')
    os.environ['LANG'] = ':'.join(locale.getlocale())
    gettext.install('messages', locale_path)

    window = GameWindow()
    state = ViewState(ROOT_DIR)
    icon_path = os.path.join(state.image_dir, 'ui', 'icon.ico')
    icon = pyglet.image.load(icon_path)
    window.set_icon(icon)

    view = MainMenuView(window, state)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
