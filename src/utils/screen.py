""" Screen utils """
import pyglet

from utils.utils import natural_keys


def supported_screen_resolutions() -> list:
    """
    Get supported screen resolutions for launcher
    @return: list of string
    """
    modes = filter(lambda x: x.height >= 720, pyglet.canvas.get_display().get_default_screen().get_modes())

    mode_values = []

    for mode in modes:
        item = str(mode.width) + "x" + str(mode.height)
        if item not in mode_values:
            mode_values.append(item)

    return sorted(mode_values, key=natural_keys)


def antialiasing() -> tuple:
    return 0, 2, 4, 8, 16
