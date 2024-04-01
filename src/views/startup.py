""" Grunzi game Startup """
import argparse
import gettext
import locale
import logging
import os

import pyglet

from constants.audio import DEFAULT_AUDIO_BACKEND, AUDIO_BACKENDS
from constants.display import UNLIMITED_FRAMERATE
from constants.maps import FIRST_MAP
from state.settingsstate import SettingsState
from state.viewstate import ViewState
from utils.log import log_hardware_info, configure_logger
from utils.text import label_value
from views.intro import Intro
from views.mainmenu import MainMenu
from window.gamewindow import SCREEN_WIDTH, SCREEN_HEIGHT, GameWindow
from window.launcherwindow import LauncherWindow


class StartUp:
    def __init__(self, root_dir: str):
        """
        Constructor
        @param root_dir: Root directory of the game
        """
        self.root_dir = root_dir

    def parse_args(self) -> argparse.Namespace:
        """
        Parse CLI args
        @return: parsed arguments
        """
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
            '--borderless',
            default=False,
            action='store_true',
            help='Borderless window'
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
            '--limit-fps',
            type=int,
            default=UNLIMITED_FRAMERATE,
            help='Limit maximum fps'
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
            choices=tuple(AUDIO_BACKENDS),
            default=DEFAULT_AUDIO_BACKEND,
            action='store',
            type=str,
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

    def setup_locale(self):
        # Set locale
        locale_path = os.path.join(self.root_dir, 'data', 'locales')
        os.environ['LANG'] = ':'.join(locale.getlocale())
        gettext.install('messages', locale_path)

    def setup_path(self):
        thirdparty_path = os.path.join(self.root_dir, 'data', '3rdparty')
        os.environ["PATH"] += os.pathsep + thirdparty_path

    def main(self):
        """Main function"""

        self.setup_locale()
        self.setup_path()

        args = self.parse_args()

        LOG_LEVEL = logging.INFO
        LOG_LEVEL_ARCADE = logging.ERROR

        if args.verbose >= 1:
            LOG_LEVEL_ARCADE = logging.INFO

        if args.verbose >= 2:
            LOG_LEVEL = logging.DEBUG
            LOG_LEVEL_ARCADE = logging.DEBUG

        if args.verbose >= 3:
            LOG_LEVEL = logging.NOTSET
            LOG_LEVEL_ARCADE = logging.NOTSET

        pyglet.options['win32_disable_shaping'] = True

        configure_logger(LOG_LEVEL)

        if args.fullscreen:
            args.window = False
        elif args.window:
            args.fullscreen = False
        else:
            args.fullscreen = True

        if not args.skip_launcher:
            launcher = LauncherWindow(args=args, state=ViewState(self.root_dir))
            launcher.setup()
            launcher.mainloop()
            if not launcher.get_args():
                return

            args = launcher.get_args()

        if args.silent:
            args.audio_backend = 'silent'

        if args.audio_backend and args.audio_backend != 'auto':
            pyglet.options['audio'] = (args.audio_backend,)

        logging.debug(label_value('Audio backend', args.audio_backend))

        import arcade

        arcade.configure_logging(level=LOG_LEVEL_ARCADE)

        logging.info(label_value('Arguments', args))
        logging.info(label_value('Pyglet options', pyglet.options))

        window = GameWindow(
            args.window,
            args.width,
            args.height,
            vsync=not args.no_vsync,
            draw_rate=args.limit_fps,
            borderless=args.borderless
        )

        log_hardware_info(window)

        window.setup()

        state = ViewState(self.root_dir, map_name=args.map, settings=SettingsState.load())
        state.preload()
        icon_path = os.path.join(state.image_dir, 'ui', 'icon.ico')
        icon = pyglet.image.load(icon_path)
        window.set_icon(icon)

        view = Intro(window, state)

        if args.skip_logo:
            view = MainMenu(window, state)

        window.show_view(view)
        arcade.run()
