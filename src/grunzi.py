#!/usr/bin/env python3

"""
Grunzi launch file
"""
import argparse
import gettext
import locale
import logging
import os
import sys

import pyglet

from constants.maps import FIRST_MAP
from state.settingsstate import SettingsState
from state.viewstate import ViewState
from utils.log import configure_logger, log_hardware_info
from utils.text import label_value
from views.intro import Intro
from views.mainmenu import MainMenu
from window.gamewindow import GameWindow, SCREEN_WIDTH, SCREEN_HEIGHT
from window.launcherwindow import LauncherWindow

ROOT_DIR = os.path.dirname(__file__)

# extend path for ffmpeg
THIRDPARTY_DIR = os.path.join(ROOT_DIR, 'data', '3rdparty')
os.environ["PATH"] += os.pathsep + THIRDPARTY_DIR


def cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--window',
        action='store_true',
        default=False,
        help='Run in windowed mode'
    )

    parser.add_argument(
        '--fullscreen',
        action='store_true',
        default=False,
        help='Run in fullscreen mode'
    )

    parser.add_argument(
        '--width',
        type=int,
        default=SCREEN_WIDTH,
        help='Window width in pixels'
    )

    parser.add_argument(
        '--height',
        type=int,
        default=SCREEN_HEIGHT,
        help='Window height in pixels'
    )

    parser.add_argument(
        '--map',
        type=str,
        default=FIRST_MAP,
        help='Name of the map'
    )

    parser.add_argument(
        '--silent',
        default=False,
        action='store_true',
        help='Mute the sound'
    )

    parser.add_argument(
        '--audio-backend',
        type=str,
        default='auto',
        choices=[
            'auto',
            'openal',
            'xaudio2',
            'directsound',
            'pulse',
            'silent'
        ],
        help='The audio backend'
    )

    parser.add_argument(
        '--no-vsync',
        action='store_true',
        default=False,
        help='Disable V-Sync'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        default=0,
        action='count',
        help='Make the operation more talkative'
    )

    parser.add_argument(
        '-l',
        '--skip-logo',
        action='store_true',
        help='Skip the logo screen and go straight to main menu'
    )

    parser.add_argument(
        '--skip-launcher',
        action='store_true',
        default=False,
        help='Skip launcher'
    )

    return parser.parse_args()


def setup_locale():
    # Set locale
    locale_path = os.path.join(ROOT_DIR, 'data', 'locales')
    os.environ['LANG'] = ':'.join(locale.getlocale())
    gettext.install('messages', locale_path)


def main():
    """Main function"""
    setup_locale()
    args = cli_args()

    LOG_LEVEL = logging.INFO

    if args.verbose >= 1:
        LOG_LEVEL = logging.DEBUG

    if args.verbose >= 2:
        LOG_LEVEL = logging.NOTSET

    configure_logger(LOG_LEVEL)

    if args.fullscreen:
        args.window = False
    elif args.window:
        args.fullscreen = False
    else:
        args.fullscreen = True

    if not args.skip_launcher:
        launcher = LauncherWindow(args=args, state=ViewState(ROOT_DIR))
        launcher.setup()
        launcher.mainloop()
        if not launcher.get_args():
            return

        args = launcher.get_args()

    if args.silent:
        args.audio_backend = 'silent'

    if args.audio_backend and args.audio_backend != 'auto':
        pyglet.options['audio'] = args.audio_backend

    pyglet.options['shadow_window'] = True

    import arcade

    logging.info(label_value('Arguments', args))
    logging.info(label_value('Pyglet options', pyglet.options))

    window = GameWindow(
        args.window,
        args.width,
        args.height,
        vsync=not args.no_vsync
    )

    log_hardware_info(window)

    window.setup()

    state = ViewState(ROOT_DIR, map_name=args.map, settings=SettingsState.load())
    state.preload()
    icon_path = os.path.join(state.image_dir, 'ui', 'icon.ico')
    icon = pyglet.image.load(icon_path)
    window.set_icon(icon)

    view = Intro(window, state)

    if args.skip_logo:
        view = MainMenu(window, state)

    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        sys.exit()
    except Exception as e:
        logging.fatal("Fatal exception", exc_info=e)
        sys.exit()
