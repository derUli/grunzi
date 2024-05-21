""" Audio utils """

import logging
import os
import random

import arcade

from utils.path import is_windows

AUDIO_EXTENSIONS = ['.ogg']


class MusicQueue:
    """ Queue used to play randomized background music """

    def __init__(self, state, files=None):
        """
        Constructor
        @param state: view state
        @param files: list of files to play
        """
        if files is None:
            files = []
        self.files = files
        self.queue = []
        self.music = None
        self.player = None
        self.state = state

    def set_files(self, files: list) -> None:
        """
        Set the files to play
        @param files: list of files
        """
        self.files = files

    def from_directory(self, path: str) -> None:
        """
        Fill queue from a directory of audio files
        @param path: directory path containing audio files
        """
        if not os.path.exists(path):
            return

        files = sorted(os.listdir(path))
        self.files = []
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in AUDIO_EXTENSIONS:
                abspath = os.path.join(path, file)
                self.files.append(abspath)

    def shuffle(self) -> None:
        """
        Shuffle the playlist
        """
        self.queue = list(self.files)
        random.shuffle(self.queue)

    def play(self):
        """
        Start the music queue
        @return:
        """
        if self.player:
            self.player.play()
            return

        self.next()

    def pause(self) -> None:
        """
        Pause the queue
        """
        if self.player:
            self.player.pause()

    def next(self) -> None:
        """
        Play the next song
        @return:
        """
        if len(self.queue) == 0:
            self.shuffle()

        if self.player:
            self.player.pop_handlers()

        if len(self.queue) == 0:
            return

        self.music = arcade.load_sound(self.queue[0])
        self.player = self.music.play(volume=self.state.settings.music_volume)
        self.queue = self.queue[1:]

        # Play the next song after the old song is completed
        self.player.push_handlers(on_eos=self.next)

    def update(self) -> None:
        """ Update volume if changed """
        if not self.player:
            return

        if self.player.volume != self.state.settings.music_volume:
            self.player.volume = self.state.settings.music_volume

            logging.info(f"Music volume at {self.state.settings.music_volume}")


def normalize_volume(volume: float) -> float:
    """
    Normalize volume

    @param volume: volume
    @return: normalized volume
    """
    volume = round(volume, 2)
    if volume > 1.0:
        volume = 1.0

    if volume < 0.0:
        volume = 0.0

    return volume


def streaming_enabled() -> bool:
    """ Linux OGG playback with streaming has timing issues """
    return is_windows()
