""" Other utility functions """
import re

from utils.path import is_windows


WIN_SCREENSAVER_DISABLE = 0x80000002
WIN_SCREENSAVER_ENABLE = 0x80000000

def atoi(text):
    return int(text) if text.isdigit() else text.lower()


def natural_keys(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    """
    return [atoi(c) for c in re.split('(\d+)', text)]


def disable_screensaver(disable=True):
    """ Disables the fullscreen on windows """
    if not is_windows():
        return None

    import ctypes
    value = 0x80000002

    if not disable:
        value = 0x80000000

    return ctypes.windll.kernel32.SetThreadExecutionState(value)  # this will prevent the screen saver or sleep.
