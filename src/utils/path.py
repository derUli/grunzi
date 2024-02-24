import os


def is_windows() -> bool:
    """ Check if we are on Windows """
    return os.name == 'nt'

GAMEDIR_NAME_WINDOWS = 'Grunzi'
GAMEDIR_NAME_LINUX = '.grunzi'

def get_userdata_path() -> str:
    """ Get savegame dir """
    homedir = os.path.expanduser('~')
    userdata_dir = os.path.join(homedir, GAMEDIR_NAME_LINUX)

    if is_windows():
        userdata_dir = os.path.join(
            homedir,
            'Documents',
            'My Games',
            GAMEDIR_NAME_WINDOWS
        )

    return userdata_dir