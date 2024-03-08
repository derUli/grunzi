import logging

MAX_DISTANCE = 800
FADE_SPEED = 0.1

import arcade


class PositionalSound:
    def __init__(self, listener, source, player, state):
        self.listener = listener
        self.source = source
        self.state = state
        self.player = player

        if self.player:
            self.player.volume = 0

    def update(self):
        if not self.player:
            return

        if not self.player.playing:
            return

        distance = arcade.get_distance_between_sprites(self.listener, self.source)
        distance = abs(distance)

        # Final volume = normalized sound volume × (max distance - distance) / max distance
        volume = self.player.volume

        if distance <= MAX_DISTANCE:
            volume = min(volume + FADE_SPEED, 1.0)
        else:
            volume = max(volume - FADE_SPEED, 0)

        volume = round(volume * self.state.sound_volume, 2)

        if volume != self.player.volume:
            logging.debug('Volume at %s', volume)
            self.player.volume = volume

    def pause(self):
        if not self.player:
            return

        self.player.pause()

    def play(self):
        if not self.player:
            return

        self.player.play()
