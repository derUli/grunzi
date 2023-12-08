import logging
import os
import time
from threading import Thread

import pygame
from PygameShader.shader import bilinear

import utils.quality
from constants.graphics import SPRITE_SIZE
from utils.string import natural_keys

TRANSPARENT_IMAGES = ['.png', '.gif']
IMAGE_EXTENSIONS = ['.jpg', '.bmp'] + TRANSPARENT_IMAGES

CHUNK_SIZE = 10


class Animation:

    def __init__(self, animation_dir, refresh_interval=0.1, start_frame=0, size=None, loop=True):
        """ Constructor """

        self.current_frame = start_frame
        self.refresh_interval = refresh_interval
        self.files = []
        self.frames = []
        self.loaded = False
        self.last_refresh = time.time()
        self.size = size
        self.loop = loop

        files = sorted(os.listdir(animation_dir), key=natural_keys)

        for file in files:
            extension = os.path.splitext(file)[1]
            if extension.lower() in IMAGE_EXTENSIONS:
                fullpath = os.path.join(animation_dir, file)
                self.files.append(fullpath)

    def load(self):
        self.loaded = True
        """ Reload frames """
        logging.debug('Async reload animation started')
        thread = Thread(target=self.load_async)
        thread.start()
        logging.debug('Async reload animation finished')

    def load_async(self):
        """ Load all animation files """
        for file in self.files:
            self.frames += [self.load_frame(file)]

    def reload(self):
        """ Reload frames """
        self.loaded = True
        logging.debug('Async reload animation started')
        thread = Thread(target=self.reload_async)
        thread.start()
        logging.debug('Async reload animation finished')

    def fully_loaded(self):
        """ Check if animation is fully loaded """
        return len(self.frames) == len(self.files)

    def reload_async(self):
        frames = []
        for file in self.files:
            frames += [self.load_frame(file)]

        self.frames = frames

    def load_frame(self, file):
        """" Load images """
        frame = pygame.image.load(file)

        extension = os.path.splitext(file)[1]

        is_alpha = False

        scale_fn = utils.quality.scale_method()

        if extension in TRANSPARENT_IMAGES:
            frame = frame.convert_alpha()
            is_alpha = True
        else:
            frame = frame.convert()

        if self.size:
            if not is_alpha and self.size < frame.get_size():
                scale_fn = bilinear
            frame = scale_fn(
                frame,
                self.size
            )

        return frame

    def empty_surface(self):
        """ Returns an empty surface """
        return pygame.surface.Surface(SPRITE_SIZE).convert_alpha()

    def get_frame(self):
        if not self.loaded:
            self.load()
            return self.empty_surface()

        try:
            frame = self.frames[self.current_frame]
        except IndexError as e:
            return self.empty_surface()

        if time.time() - self.last_refresh < self.refresh_interval:
            return frame

        next_frame = self.current_frame + 1

        if next_frame >= len(self.files) and self.loop:
            next_frame = 0

        if next_frame >= len(self.frames):
            next_frame = self.current_frame

        self.current_frame = next_frame
        self.last_refresh = time.time()

        return frame

    def has_more_frames(self):
        return self.current_frame + 1 < len(self.files)
