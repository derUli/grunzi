""" Used to store pressed keys"""

class KeyPressed:
    """ Class to store pressed keys"""

    def __init__(self):
        """ Constructor """

        self.key_up = False
        self.key_right = False
        self.key_down = False
        self.key_left = False

    def reset(self):
        """ Reset values """

        self.key_up = False
        self.key_right = False
        self.key_down = False
        self.key_left = False
