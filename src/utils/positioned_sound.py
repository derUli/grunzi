import arcade


class PositionedSound:
    def __init__(self, listener, source, sound, state):
        self.listener = listener
        self.source = source
        self.sound = sound
        self.state = state
        self.player = None

    def start(self, loop=False):
        self.player = self.sound.play(volume=self.state.sound_volume, loop=loop)

    def update(self):
        distance = arcade.get_distance_between_sprites(self.listener, self.source)
        distance = abs(distance)
        print(distance)