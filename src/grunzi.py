"""
Grunzi launch file
"""
import argparse
import gettext
import locale
import logging
import os

import arcade
import pyglet

from state.viewstate import ViewState
from utils.logging import configure_logger
from utils.text import label_value
from views.intro import Intro

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

    def __init__(
            self,
            window=False,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            debug=False,
            update_rate=1 / 60
    ):
        # Call the parent class and set up the window
        super().__init__(
            width=width,
            height=height,
            title=SCREEN_TITLE,
            fullscreen=False,
            vsync=True,
            update_rate=update_rate,
            antialiasing=False,
            samples=4
        )

        self.set_fullscreen(not window)

        self.update_rate = update_rate
        self.draw_rate = update_rate

        self.debug = debug

        if debug:
            arcade.enable_timings()

    def set_fullscreen(self, fullscreen=True):
        screen = pyglet.canvas.get_display().get_default_screen()
        mode = screen.get_closest_mode(self.width, self.height)

        return super().set_fullscreen(fullscreen=fullscreen, screen=screen, mode=mode)


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
        '--debug',
        action='store_true',
        default=False,
        help=_('Enable debug mode')
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

    parser.add_argument(
        '--map',
        type=str,
        default='world',
        help=_('Name of the map')
    )

    parser.add_argument(
        '--silent',
        default=False,
        action='store_true',
        help=_('Mute the sound')
    )

    parser.add_argument(
        '-v',
        '--verbose',
        default=0,
        action='count',
        help=_('Make the operation more talkative')
    )

    args = parser.parse_args()

    if args.silent:
        pyglet.options['audio'] = 'silent'

    pyglet.options['debug_gl'] = args.debug

    LOG_LEVEL = logging.INFO

    if args.verbose >= 1:
        LOG_LEVEL = logging.DEBUG

    if args.verbose >= 2:
        LOG_LEVEL = logging.NOTSET

    configure_logger(LOG_LEVEL)
    logging.info(label_value(_('Arguments'), args))
    logging.info(label_value(_('Pyglet options'), pyglet.options))

    window = GameWindow(args.window, args.width, args.height, debug=args.debug)
    state = ViewState(ROOT_DIR, map_name=args.map)
    state.preload()
    icon_path = os.path.join(state.image_dir, 'ui', 'icon.ico')
    icon = pyglet.image.load(icon_path)
    window.set_icon(icon)

    view = Intro(window, state)
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
