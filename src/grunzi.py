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
import argparse

SCREEN_TITLE = "Grunzi"

ROOT_DIR = os.path.dirname(__file__)

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

    def __init__(self, window=False, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):

        # Call the parent class and set up the window
        super().__init__(width=width, height=height, title=SCREEN_TITLE, fullscreen=not window, vsync=True)


def main():
    """Main function"""

    # Set locale
    locale_path = os.path.join(ROOT_DIR, 'data', 'locale')
    os.environ['LANG'] = ':'.join(locale.getlocale())
    gettext.install('messages', locale_path)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--window',
        action='store_true',
        default=False,
        help=_('Run in windowed mode')
    )
    parser.add_argument(
        '--width',
        type=int,
        default=SCREEN_WIDTH,
        help=_('Window width in pixels')
    )
    parser.add_argument(
        '--height',
        type=int,
        default=SCREEN_HEIGHT,
        help=_('Window height in pixels')
    )
    args = parser.parse_args()

    window = GameWindow(args.window, args.width, args.height)
    state = ViewState(ROOT_DIR)
    icon_path = os.path.join(state.image_dir, 'ui', 'icon.ico')
    icon = pyglet.image.load(icon_path)
    window.set_icon(icon)

    view = MainMenuView(window, state)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()
