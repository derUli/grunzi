import os
import random

import arcade

AUDIO_EXTENSIONS = ['.ogg']


class MusicQueue:
    def __init__(self, files: list = []):
        if files is None:
            files = []

        self.files = files
        self.queue = []
        self.music = None
        self.player = None

    def set_files(self, files) -> None:
        self.files = files

    def from_directory(self, dir) -> None:
        files = sorted(os.listdir(dir))
        self.files = []
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in AUDIO_EXTENSIONS:
                abspath = os.path.join(dir, file)
                self.files.append(abspath)

    def shuffle(self) -> None:
        self.queue = list(self.files)
        random.shuffle(self.queue)

    def play(self):
        if self.player:
            self.player.play()
            return

        self.next()

    def pause(self):
        self.player.pause()

    def next(self) -> None:
        if len(self.queue) == 0:
            self.shuffle()

        if self.player:
            self.player.pop_handlers()

        self.music = arcade.load_sound(self.queue[0], streaming=True)
        self.player = self.music.play()
        self.queue = self.queue[1:]

        self.player.push_handlers(on_eos=self.next)
