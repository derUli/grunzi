#!/usr/bin/env python3

"""
Grunzi launch file
"""
import argparse
import gettext
import locale
import logging
import os
import signal
import sys

import pyglet

from state.viewstate import ViewState
from utils.log import configure_logger, log_hardware_info
from utils.text import label_value
from views.intro import Intro
from window.gamewindow import GameWindow, SCREEN_WIDTH, SCREEN_HEIGHT
from window.launcherwindow import LauncherWindow

ROOT_DIR = os.path.dirname(__file__)


def cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--window',
        action='store_true',
        default=False,
        help=_('Run in windowed mode')
    )

    parser.add_argument(
        '--fullscreen',
        action='store_true',
        default=False,
        help=_('Run in fullscreen mode')
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

    parser.add_argument(
        '--skip-launcher',
        action='store_true',
        default=False,
        help=_('Skip launcher')
    )

    return parser.parse_args()


def setup_locale():
    # Set locale
    locale_path = os.path.join(ROOT_DIR, 'data', 'locale')
    os.environ['LANG'] = ':'.join(locale.getlocale())
    gettext.install('messages', locale_path)


def signal_handler(signal, frame):
    sys.exit()


def main():
    # Kill and interrupt handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGILL, signal_handler)

    """Main function"""
    setup_locale()
    args = cli_args()

    LOG_LEVEL = logging.INFO

    if args.verbose >= 1:
        LOG_LEVEL = logging.DEBUG

    if args.verbose >= 2:
        LOG_LEVEL = logging.NOTSET

    configure_logger(LOG_LEVEL)
    log_hardware_info()

    if args.fullscreen:
        args.window = False
    elif args.window:
        args.fullscreen = False
    else:
        args.fullscreen = True

    if not args.skip_launcher:
        launcher = LauncherWindow(args, ViewState(ROOT_DIR))
        launcher.setup()
        launcher.mainloop()

        if not launcher.get_args():
            return

        args = launcher.get_args()

    if args.silent:
        pyglet.options['audio'] = 'silent'

    pyglet.options['debug_gl'] = args.debug
    pyglet.options["xinput_controllers"] = False

    import arcade

    logging.info(label_value(_('Arguments'), args))
    logging.info(label_value(_('Pyglet options'), pyglet.options))

    window = GameWindow(args.window, args.width, args.height, debug=args.debug)
    window.setup()

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
