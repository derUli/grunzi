import pygame
import os
import time

IMAGE_EXTENSIONS = ['.jpg', '.png', '.gif']


class Animation():

    def __init__(self, animation_dir, refresh_interval=0.1,
                 start_frame=0, size=None, async_load=True):
        """ Constructor """

        self.current_frame = start_frame
        self.refresh_interval = refresh_interval
        self.files = []
        self.frames = []
        self.loaded = False
        self.last_refresh = time.time()
        self.size = size
        self.async_load = async_load
        self.load_chunks = 5

        files = sorted(os.listdir(animation_dir))

        for file in files:
            extension = os.path.splitext(file)[1]
            if extension.lower() in IMAGE_EXTENSIONS:
                fullpath = os.path.join(animation_dir, file)
                self.files.append(fullpath)

    def load(self):
        for file in self.files:
            frame = pygame.image.load(file).convert_alpha()

            if self.size:
                frame = pygame.transform.smoothscale(
                    frame,
                    self.size
                )

            self.frames.append(frame)

            if self.async_load:
                self.files = self.files[1:]
                return

        self.loaded = True

    def get_frame(self):
        if not self.loaded:
            self.load()

        frame = self.frames[self.current_frame]

        if time.time() - self.last_refresh < self.refresh_interval:
            return frame

        next_frame = self.current_frame + 1

        if next_frame >= len(self.frames):
            next_frame = 0

        self.current_frame = next_frame
        self.last_refresh = time.time()

        return frame
