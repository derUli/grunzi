VOLUME_QUANTITY = 0.001

import arcade
class PositionedSound:
    def __init__(self, listener, source, player, state):
        self.listener = listener
        self.source = source
        self.state = state
        self.player = player

    def update(self):
        distance = arcade.get_distance_between_sprites(self.listener, self.source)
        distance = abs(distance)

        volume = 1 - (distance * VOLUME_QUANTITY)
        volume = volume * self.state.sound_volume
        volume = round(volume, 2)

        if volume < 0.0:
            volume = 0.0

        if volume != self.player.volume:
            self.player.volume = volume
