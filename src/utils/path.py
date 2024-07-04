""" User path utils """

import os
import platform

GAMEDIR_NAME_WINDOWS = 'Grunzi'
GAMEDIR_NAME_LINUX = '.grunzi'


def is_windows() -> bool:
    """ Check if we are on Windows """
    return os.name == 'nt'


def is_linux() -> bool:
    """ Check if we are on Linux """
    return platform.system() == 'Linux'


def get_userdata_path() -> str:
    """
    Get userdata path
    @return: userdata path
    """
    homedir = os.path.expanduser('~')
    userdata_dir = os.path.join(homedir, GAMEDIR_NAME_LINUX)

    if is_windows():
        userdata_dir = os.path.join(
            homedir,
            'Documents',
            'My Games',
            GAMEDIR_NAME_WINDOWS
        )

    # If the directory doesn't exists create it
    os.makedirs(userdata_dir, exist_ok=True)

    return userdata_dir


def get_settings_path():
    """
    Get settings file path
    @return: userdata path
    """
    path = os.path.join(get_userdata_path())

    os.makedirs(path, exist_ok=True)

    return os.path.join(path, 'settings.json')


def get_log_path() -> str:
    """
    Get savegame file path
    @return: userdata path
    """
    path = os.path.join(get_userdata_path(), 'logs')

    os.makedirs(path, exist_ok=True)
    return path


def get_savegame_path(name: str) -> str:
    """
    Get savegame file path
    @return: userdata path
    """
    path = os.path.join(get_userdata_path(), 'savegames', name + '.json')
    path = os.path.join(get_userdata_path(), 'savegames', name + '.json')

    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def get_autodetect_path() -> str:
    """
    Get path to the file containg the autodetected quality
    @return: filename
    """
    return os.path.join(get_userdata_path(), 'autodetect.txt')


def get_user():
    return os.environ.get('USER', os.environ.get('USERNAME'))
