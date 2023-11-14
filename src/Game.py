""" Grunzi Game Launcher """
import argparse
import gettext
import locale
import logging
import os
import time

# os.environ['PYGAME_BLEND_ALPHA_SDL2'] = '1'

from bootstrap.gamecontainer import GameContainer
from components.maingame import MainGame
from components.menu import Menu
from utils.path import get_userdata_path

__main__ = __file__

root_dir = os.path.join(os.path.dirname(__main__))
locale_path = os.path.join(root_dir, 'data', 'locale')

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
    '-d',
    '--disable-controller',
    action='store_true',
    help='Disable controller support'
)

args = parser.parse_args()

# While still in alpha the log level is always debug
# TODO: Remove before production release
args.debug = True

log_file = os.path.join(get_userdata_path(), 'debug.log')

log_level = logging.INFO

if args.debug:
    log_level = logging.DEBUG

logging.basicConfig(
    level=log_level,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logging.debug(args)

game = GameContainer(
    root_dir,
    enable_edit_mode=args.edit,
    disable_controller=args.disable_controller,
    disable_ai=args.disable_ai
)

game.__main__ = os.path.abspath(__main__)
game.start()
