""" Grunzi Game Launcher """
import argparse
import logging
import os
from gettext import gettext

from bootstrap.gamecontainer import GameContainer
from utils.path import get_userdata_path

_ = gettext

root_dir = os.path.join(os.path.dirname(__file__))

parser = argparse.ArgumentParser(
    prog=_('Grunzi'),
    description=_('Piggy adventure game')
)

parser.add_argument('-e', '--edit', action='store_true', help='Enable In-Game Map Editor')
parser.add_argument('-v', '--debug', action='store_true', help='Enable debug loglevel')

# Game starts by default without hardware acceleration because I couldn't get
# the game to work on my machine with pygame.OPENGL flag
parser.add_argument('-o', '--opengl', action='store_true', help='Enable OpenGL')
args = parser.parse_args()

print(args)

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

game = GameContainer(root_dir, enable_edit_mode=args.edit, opengl = args.opengl)
game.start()
