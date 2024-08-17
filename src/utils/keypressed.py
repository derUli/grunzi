""" Used to store pressed keys"""


class KeyPressed:
    """ Class to store pressed keys"""

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

    def any(self):
        return self.key_up or self.key_right or self.key_down or self.key_left
