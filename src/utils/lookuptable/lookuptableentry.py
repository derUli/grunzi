class LookupTableEntry:
    def __init__(self):
        self.position = (-1, -1)

        self.value = []

    def needs_update(self, player):
        return player.position != self.position

    def set(self, player, value):
        self.position = player.position
        self.value = value

    def get(self):
        return self.value