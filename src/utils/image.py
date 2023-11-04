import logging

import pygame


class ImageCache:

    def __init__(self):
        self.images = {}

    def load_image(self, path):
        if not path in self.images:
            try:
                self.images[path] = pygame.image.load(path).convert_alpha()
            except FileNotFoundError:
                logging.error('File not found ' + path)
                self.images[path] = None

        return self.images[path]
