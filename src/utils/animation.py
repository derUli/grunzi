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
IMAGE_EXTENSIONS = ['.jpg'] + TRANSPARENT_IMAGES

CHUNK_SIZE = 10


class Animation():

    def __init__(self, animation_dir, refresh_interval=0.1,
                 start_frame=0, size=None):
        """ Constructor """

        self.current_frame = start_frame
        self.refresh_interval = refresh_interval
        self.files = []
        self.frames = []
        self.loaded = False
        self.last_refresh = time.time()
        self.size = size

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
        for file in self.files:
            self.frames += [self.load_frame(file)]

    def reload(self):
        self.loaded = True
        """ Reload frames """
        logging.debug('Async reload animation started')
        thread = Thread(target=self.reload_async)
        thread.start()
        logging.debug('Async reload animation finished')

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

    def get_frame(self):
        empty_surface = pygame.surface.Surface(SPRITE_SIZE).convert_alpha()
        if not self.loaded:
            self.load()
            return empty_surface

        try:
            frame = self.frames[self.current_frame]
        except IndexError as e:
            return empty_surface

        if time.time() - self.last_refresh < self.refresh_interval:
            return frame

        next_frame = self.current_frame + 1

        if next_frame >= len(self.files):
            next_frame = 0

        if next_frame >= len(self.frames):
            next_frame = self.current_frame

        self.current_frame = next_frame
        self.last_refresh = time.time()

        return frame
