class LookupTableEntry:
    def __init__(self):
        self.position = (-1, -1)

        self._value = []

    def needs_update(self, player_sprite):
        return player_sprite.position != self.position

    def set(self, value, player_sprite):
        self.position = player_sprite.position
        self._value = value

    def get(self):
        return self._value
