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

root_dir = os.path.join(os.path.dirname(__file__))

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

parser.add_argument(
    '-s',
    '--skip-menu',
    action='store_true',
    help='Skip menu'
)

parser.add_argument(
    '-b',
    '--benchmark',
    help='Do benchmark',
    type=int,
    required=False
)

args = parser.parse_args()

log_file = os.path.join(get_userdata_path(), 'debug.log')

log_level = logging.INFO

if args.benchmark:
    args.skip_menu = True

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

component = Menu

if args.skip_menu:
    component = MainGame

game = GameContainer(
    root_dir,
    enable_edit_mode=args.edit,
    disable_controller=args.disable_controller,
    disable_ai=args.disable_ai
)

if args.benchmark:
    minutes = args.benchmark
    hours = round(minutes / 60, 2)
    print('Do benchmark for ' + str(hours) + " hours")
    seconds = minutes * 60

    game.do_benchmark = time.time() + seconds

game.start(component)
