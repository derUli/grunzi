import random
import os
import pygame
from threading import Thread
AUDIO_EXTENSIONS = ['.ogg']

class MusicQueue:
    def __init__(self, files=[]):
        self.files = files
        self.queue = []

    def set_files(self, files):
        self.files = files

    def from_directory(self, dir):
        files = sorted(os.listdir(dir))
        self.files = []
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in AUDIO_EXTENSIONS:
                abspath = os.path.join(dir, file)
                self.files.append(abspath)


    def shuffle(self):
        self.queue = list(self.files)
        random.shuffle(self.queue)

    def play(self):
        self.playing = True
        self.next()

    def stop(self):
        self.playing = False
        pygame.mixer.music.stop()

    def pause(self):
        pygame.mixer.music.pause()

    def check_for_next(self):
        if not self.playing:
            return

        if not pygame.mixer.music.get_busy():
            self.next()

    def next(self):
        if len(self.queue) == 0:
            self.shuffle()

        pygame.mixer.music.load(self.queue[0])
        pygame.mixer.music.play()
        self.queue = self.queue[1:]

