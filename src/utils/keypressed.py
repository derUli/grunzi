""" Used to store pressed keys"""

from constants.controls.keyboard import KEY_MOVE_UP, KEY_MOVE_RIGHT, KEY_MOVE_DOWN, KEY_MOVE_LEFT


class KeyPressed:
    """ Class to store pressed keys """

    def __init__(self):
        """ Constructor """

        self.key_up = False
        self.key_right = False
        self.key_down = False
        self.key_left = False

    def reset(self) -> None:
        """ Reset values """

        self.key_up = False
        self.key_right = False
        self.key_down = False
        self.key_left = False

    @property
    def key_pressed(self) -> bool:
        """ Is key pressed """

        return self.key_up or self.key_right or self.key_down or self.key_left

    def on_key_press(self, key) -> None:
        if key in KEY_MOVE_LEFT:
            self.key_left = True
        if key in KEY_MOVE_RIGHT:
            self.key_right = True
        if key in KEY_MOVE_UP:
            self.key_up = True
        if key in KEY_MOVE_DOWN:
            self.key_down = True

    def on_key_release(self, key) -> None:
        if key in KEY_MOVE_LEFT:
            self.key_left = False
        if key in KEY_MOVE_RIGHT:
            self.key_right = False
        if key in KEY_MOVE_UP:
            self.key_up = False
        if key in KEY_MOVE_DOWN:
            self.key_down = False
