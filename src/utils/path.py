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

    if not os.path.exists(userdata_dir):
        os.makedirs(userdata_dir)

    return userdata_dir

def get_settings_path():
    return os.path.join(get_userdata_path(), 'settings.json')
