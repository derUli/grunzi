import logging
import os
import time
from threading import Thread

import pygame

import utils.quality
from constants.graphics import SPRITE_SIZE
from utils.string import natural_keys

TRANSPARENT_IMAGES = ['.png', '.gif']
IMAGE_EXTENSIONS = ['.jpg', '.bmp'] + TRANSPARENT_IMAGES


class Animation:

    def __init__(self, animation_dir, refresh_interval=0.1,
                 start_frame=0, size=None, loop=True):
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

    def load_async(self):
        """ Load animation filles async """
        self.loaded = True
        logging.debug('Async reload animation started')
        thread = Thread(target=self.load_sync)
        thread.start()
        logging.debug('Async reload animation finished')

    def reload_sync(self):
        """ Load all animation files """
        frames = []
        for file in self.files:
            try:
                frames += [self.load_frame(file)]
            except pygame.error as e:
                logging.error(e)
                return

        self.frames = frames

    def load_sync(self):
        """ Load all animation files """
        for file in self.files:
            try:
                self.frames += [self.load_frame(file)]
            except pygame.error as e:
                logging.error(e)
                return

    def reload(self):
        self.reload_async()

    def reload_async(self):
        """ Reload frames """
        self.loaded = True
        logging.debug('Async reload animation started')
        thread = Thread(target=self.reload_sync)
        thread.start()
        logging.debug('Async reload animation finished')

    def fully_loaded(self):
        """ Check if animation is fully loaded """
        return len(self.frames) == len(self.files)

    def load_frame(self, file):
        """" Load images """
        frame = pygame.image.load(file)

        extension = os.path.splitext(file)[1]

        scale_fn = utils.quality.scale_method()

        if extension in TRANSPARENT_IMAGES:
            frame = frame.convert_alpha()
        else:
            frame = frame.convert()

        if self.size:
            frame = scale_fn(
                frame,
                self.size
            )

        return frame

    def empty_surface(self):
        """ Returns an empty surface """
        return pygame.surface.Surface(SPRITE_SIZE, pygame.SRCALPHA)

    def get_frame(self):
        """ Get current frame """
        if not self.loaded:
            self.load_async()
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
        """ Check if the animation has more frames """
        return self.current_frame + 1 < len(self.files)
