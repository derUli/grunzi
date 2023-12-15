import os

from constants.game import GAMEDIR_NAME_WINDOWS, GAMEDIR_NAME_LINUX


def is_windows():
    """ Check if we are on Windows """
    return os.name == 'nt'


def get_userdata_path():
    """ Get savegame dir """
    homedir = os.path.expanduser('~')

    if is_windows():
        homedir = os.path.join(homedir, 'Documents', 'My Games', GAMEDIR_NAME_WINDOWS)
    else:
        homedir = os.path.join(homedir, GAMEDIR_NAME_LINUX)

    return homedir
