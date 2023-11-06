import logging
import os.path
import utils.quality
import pygame
from constants.graphics import ALPHA_IMAGE_FORMATS

class ImageCache:

    def __init__(self):
        self.images = {}

    def clear(self):
        self.images = {}

    def load_image(self, path, scale = None):
        extension = os.path.splitext(path)[1]
        is_alpha = extension.lower() in ALPHA_IMAGE_FORMATS

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
                    image = utils.quality.scale_method()(image, scale)
                self.images[cache_id] = image
            except FileNotFoundError:
                logging.error('File not found ' + path)
                self.images[cache_id] = None

        return self.images[cache_id]
