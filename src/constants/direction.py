""" Direction constants """

from constants import keyboard
DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3
DIRECTION_DOWN = 4

def key_to_direction(key):
    """ Maps keycode to movement direction """
    match key:
        case keyboard.K_LEFT:
            return DIRECTION_LEFT
        case keyboard.K_RIGHT:
            return DIRECTION_RIGHT
        case keyboard.K_UP:
            return DIRECTION_UP
        case keyboard.K_DOWN:
            return DIRECTION_DOWN
        case _:
            return None