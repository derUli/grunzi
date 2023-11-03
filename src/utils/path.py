import os

from constants.game import GAMEDIR_NAME


def is_windows():
    return os.name == 'nt'


def get_userdata_path():
    import os
    homedir = os.path.expanduser('~')

    if is_windows():
        return os.path.join(homedir, 'Documents', 'My Games', GAMEDIR_NAME)

    return os.path.join(homedir, '.' + GAMEDIR_NAME)
