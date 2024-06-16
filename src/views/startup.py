""" Grunzi game Startup """
import argparse
import gettext
import locale
import logging
import os

import pyglet

from constants.audio import DEFAULT_AUDIO_BACKEND, audio_backends
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

    @staticmethod
    def parse_args() -> argparse.Namespace:
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
            '--silent',
            default=False,
            action='store_true',
            help='Mute the sound'
        )

        parser.add_argument(
            '--audio-backend',
            choices=tuple(audio_backends()),
            default=DEFAULT_AUDIO_BACKEND,
            action='store',
            type=str,
            help='The audio backend'
        )

        parser.add_argument(
            '--antialiasing',
            action='store',
            type=int,
            help='The antialiasing level',
            choices=tuple([0, 2, 4, 8, 16])
        )

        parser.add_argument(
            '--no-vsync',
            action='store_true',
            default=False,
            help='Disable V-Sync'
        )

        parser.add_argument(
            '--debug',
            action='store_true',
            default=False,
            help='Enable OpenGL debugging'
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

    def setup_locale(self) -> None:
        """ setup locale """

        locale_path = os.path.join(self.root_dir, 'data', 'locales')
        os.environ['LANG'] = ':'.join(locale.getlocale())
        gettext.install('messages', locale_path)

    def setup_path(self) -> None:
        """ Add third party executable directory to PATH """

        thirdparty_path = os.path.join(self.root_dir, 'data', '3rdparty')
        os.environ["PATH"] += os.pathsep + thirdparty_path

    def main(self) -> None:
        """ Main function """

        self.setup_locale()
        self.setup_path()

        args = self.parse_args()

        log_level = self.get_log_level(args.verbose)
        log_level_arcade = self.get_log_level_arcade(args.verbose)

        configure_logger(log_level)

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

        pyglet.options['debug_gl'] = args.debug
        pyglet.options['debug_trace_flush'] = args.debug

        import arcade

        arcade.configure_logging(level=log_level_arcade)

        logging.info(label_value('Arguments', args))
        logging.info(label_value('Pyglet options', pyglet.options))

        settings = SettingsState.load()

        if args.antialiasing is not None:
            settings.antialiasing = args.antialiasing
            settings.save()

        window = GameWindow(
            args.window,
            args.width,
            args.height,
            vsync=not args.no_vsync,
            draw_rate=args.limit_fps,
            borderless=args.borderless,
            antialiasing=settings.antialiasing > 0,
            samples=settings.antialiasing
        )

        log_hardware_info(window)

        window.setup()

        state = ViewState(self.root_dir, map_name=FIRST_MAP, settings=SettingsState.load())
        state.preload()
        icon_path = os.path.join(state.ui_dir, 'icon.ico')
        icon = pyglet.image.load(icon_path)
        window.set_icon(icon)

        view = Intro(window, state)

        if args.skip_logo:
            view = MainMenu(window, state)

        window.show_view(view)
        arcade.run()

    @staticmethod
    def get_log_level(verbose: int) -> int:
        """
        Get log level
        @param verbose: verbose value
        @return: Log Level
        """

        if verbose >= 3:
            return logging.NOTSET

        if verbose >= 2:
            return logging.DEBUG

        return logging.INFO

    @staticmethod
    def get_log_level_arcade(verbose: int) -> int:
        """
        Get arcade log level
        @param verbose: verbose value
        @return: Log Level
        """
        if verbose >= 3:
            return logging.NOTSET

        if verbose >= 2:
            return logging.DEBUG

        if verbose >= 1:
            return logging.INFO

        return logging.ERROR
