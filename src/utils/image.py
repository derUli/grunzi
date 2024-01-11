import logging
import os.path
import time

import pygame

from constants.graphics import ALPHA_IMAGE_FORMATS
from utils.quality import scale_method


class ImageCache:

    def __init__(self):
        self.images = {}
        self.processed_images = {}

    def clear(self):
        self.images = {}
        self.processed_images = {}

    def add_processed_image(self, name, surface):
        self.processed_images[name] = surface

    def get_processed_image(self, name):
        if name in self.processed_images:
            return self.processed_images[name]

        return None

    def load_image(self, path, scale=None):
        time.time()
        extension = os.path.splitext(path)[1]
        is_alpha = extension.lower() in ALPHA_IMAGE_FORMATS

        scale_fn = scale_method()

        cache_id = path
        if scale:
            x, y = scale

            cache_id = cache_id + '-' + str(x) + '-' + str(y)

        if cache_id not in self.images:
            try:
                image = pygame.image.load(path)

                if is_alpha:
                    image = image.convert_alpha()
                else:
                    image = image.convert()

                if scale:
                    image = scale_fn(image, scale)

                self.images[cache_id] = image

            except FileNotFoundError:
                logging.error(' '.join(['File not found', path]))
                self.images[cache_id] = None

        return self.images[cache_id]
