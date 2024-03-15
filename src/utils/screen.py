import pyglet

from utils.utils import natural_keys


def supported_screen_resolutions():
    modes = pyglet.canvas.get_display().get_default_screen().get_modes()

    mode_values = []

    for mode in modes:
        item = str(mode.width) + "x" + str(mode.height)
        if item not in mode_values:
            mode_values.append(item)

    return sorted(mode_values, key=natural_keys)
