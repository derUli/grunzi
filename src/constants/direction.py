""" Direction constants """

from constants import keyboard

DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3
DIRECTION_DOWN = 4


def key_to_direction(key):
    """ Maps keycode to movement direction """
    if key in keyboard.K_UP:
        return DIRECTION_UP
    elif key in keyboard.K_DOWN:
        return DIRECTION_DOWN
    elif key in keyboard.K_LEFT:
        return DIRECTION_LEFT
    elif key in keyboard.K_RIGHT:
        return DIRECTION_RIGHT
