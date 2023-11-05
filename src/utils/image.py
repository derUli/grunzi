import logging

import pygame


class ImageCache:

    def __init__(self):
        self.images = {}

    def load_image(self, path, scale = None):
        cache_id = path
        if scale:
            x, y = scale

            cache_id = cache_id + '-' + str(x) + '-' + str(y)

        if cache_id not in self.images:
            try:
                image = pygame.image.load(path).convert_alpha()
                if scale:
                    image = pygame.transform.smoothscale(image, scale)
                self.images[cache_id] = image
            except FileNotFoundError:
                logging.error('File not found ' + path)
                self.images[cache_id] = None

        return self.images[cache_id]
