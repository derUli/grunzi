import os
import random
import pygame

AUDIO_EXTENSIONS = ['.ogg']


class MusicQueue:
    def __init__(self, files: list = []):
        if files is None:
            files = []

        self.files = files
        self.queue = []
        self.paused = False
        self.playing = False

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

    def play(self) -> None:
        self.playing = True
        self.paused = False
        self.next()

    def stop(self) -> None:
        self.playing = False
        self.paused = False
        pygame.mixer.music.stop()

    def pause(self) -> None:
        pygame.mixer.music.pause()
        self.paused = True

    def unpause(self) -> None:
        pygame.mixer.music.unpause()
        self.paused = False

    def check_for_next(self) -> None:
        if not self.playing:
            return

        if self.paused:
            return

        if not pygame.mixer.music.get_busy():
            self.next()

    def next(self) -> None:
        if len(self.queue) == 0:
            self.shuffle()

        pygame.mixer.music.load(self.queue[0])
        pygame.mixer.music.play()
        self.queue = self.queue[1:]
