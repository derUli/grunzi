""" Direction constants """
from typing import Union

from constants import keyboard

DIRECTION_LEFT = 1
DIRECTION_RIGHT = 2
DIRECTION_UP = 3
DIRECTION_DOWN = 4


def key_to_direction(key: int) -> Union[int, None]:
    """
    Map key code to movement direction
    @param key: key code
    @return: direction
    """
    if key in keyboard.K_UP:
        return DIRECTION_UP
    if key in keyboard.K_DOWN:
        return DIRECTION_DOWN
    if key in keyboard.K_LEFT:
        return DIRECTION_LEFT
    if key in keyboard.K_RIGHT:
        return DIRECTION_RIGHT

    return None
