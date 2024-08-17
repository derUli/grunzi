class LookupTableEntry:
    def __init__(self):
        self.position = (-1, -1)

        self._value = []

    def needs_update(self, player):
        return player.position != self.position

    def set(self, value, player):
        self.position = player.position
        self._value = value

    def get(self):
        return self._value
