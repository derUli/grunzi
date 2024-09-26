class LookupTableEntry:
    def __init__(self):
        self.position_1 = (-1, -1)
        self.position_2 = (-1, -1)
        self._value = []

    def needs_update(self, sprite1, sprite2 = None):

        check1 =  sprite1.position != self.position_1

        if sprite2 is None:
            return check1

        check2 = sprite2.position != self.position_2

        return check1 or check2


    def set(self, value, sprite1, sprite2 = None):
        self.position_1 = sprite1.position

        if sprite2 is not None:
            self.position_2 = sprite2.position

        self._value = value

    def get(self):
        return self._value


    def clear(self):
        self.position_1 = (-1, -1)
        self.position_2 = (-1, -1)
        self._value = []