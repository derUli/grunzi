#!/usr/bin/python3

""" Grunzi Game Launcher """

import argparse
import gettext
import locale
import logging
import os

from bootstrap.gamecontainer import GameContainer
from components.menu.intro import Intro
from components.menu.mainmenu import MainMenu
from utils.helper import configure_logger, enable_high_dpi
from utils.path import get_userdata_path

__main__ = __file__
ROOT_DIR = os.path.join(os.path.dirname(__main__))

# Set locale
locale_path = os.path.join(ROOT_DIR, 'data', 'locale')
os.environ['LANG'] = ':'.join(locale.getlocale())
gettext.install('messages', locale_path)


def parse_args():
    """ Parse command line args """
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
        '-i',
        '--skip-intro',
        action='store_true',
        help='Skip intro'
    )

    return parser.parse_args()


args = parse_args()

# While still in alpha the log level is always debug
# TODO: Remove before production release
args.debug = True

LOG_LEVEL = logging.INFO

if args.debug:
    LOG_LEVEL = logging.DEBUG

configure_logger(LOG_LEVEL)
logging.debug(args)

enable_high_dpi()

game = GameContainer(
    ROOT_DIR,
    enable_edit_mode=args.edit,
    disable_controller=args.disable_controller,
    disable_ai=args.disable_ai
)

game.__main__ = os.path.abspath(__main__)

component = Intro

if args.skip_intro:
    component = MainMenu

game.start(component)
