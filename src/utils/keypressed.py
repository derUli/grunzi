class KeyPressed:
    def __init__(self):
        self.key_up = False
        self.key_right = False
        self.key_down = False
        self.key_left = False

    def reset(self):
        self.key_up = False
        self.key_right = False
        self.key_down = False
        self.key_left = False
