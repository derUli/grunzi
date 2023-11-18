""" Grunzi Game Launcher """
import argparse
import gettext
import locale
import logging
import os

from utils.path import is_windows, get_userdata_path

__main__ = __file__

ROOT_DIR = os.path.join(os.path.dirname(__main__))

def configure_logger(log_level):
    log_file = os.path.join(get_userdata_path(), 'debug.log')
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def parse_args():
    locale_path = os.path.join(ROOT_DIR, 'data', 'locale')

    # Set locale
    os.environ['LANG'] = ':'.join(locale.getlocale())
    gettext.install('messages', locale_path)

    if not os.path.exists(get_userdata_path()):
        os.makedirs(get_userdata_path())

    parser = argparse.ArgumentParser(
        prog=_('Grunzi'),
        description=_('Piggy adventure game')
    )

    parser.add_argument(
        '-e',
        '--edit',
        action='store_true',
        help='Enable in-game map editor'
    )

    parser.add_argument(
        '-v',
        '--debug',
        action='store_true',
        help='Enable debug loglevel'
    )

    parser.add_argument(
        '-a',
        '--disable-ai',
        action='store_true',
        help='Disable AI'
    )

    parser.add_argument(
        '-m',
        '--enable-mouse',
        action='store_true',
        help='Enable experimental mouse support'
    )

    parser.add_argument(
        '-d',
        '--disable-controller',
        action='store_true',
        help='Disable controller support'
    )

    return parser.parse_args()


def enable_high_dpi():
    # Add support for high DPI on windows
    if not is_windows():
        return

    import ctypes

    try:
        ctypes.windll.user32.SetProcessDPIAware()
        logging.debug('SetProcessDPIAware')
    except AttributeError as e:
        logging.error(e)  # Windows XP doesn't support monitor scaling, so just do nothing


args = parse_args()

# While still in alpha the log level is always debug
# TODO: Remove before production release
args.debug = True

log_level = logging.INFO

if args.debug:
    log_level = logging.DEBUG

configure_logger(log_level)
logging.debug(args)

enable_high_dpi()
# os.environ['PYGAME_BLEND_ALPHA_SDL2'] = '1'

from bootstrap.gamecontainer import GameContainer

game = GameContainer(
    ROOT_DIR,
    enable_edit_mode=args.edit,
    disable_controller=args.disable_controller,
    disable_ai=args.disable_ai,
    enable_mouse=args.enable_mouse
)

game.__main__ = os.path.abspath(__main__)
game.start()
