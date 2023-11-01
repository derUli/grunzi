import pygame

class ImageCache:
    def __init__(self):
        self.images = {}

    def load_image(self, path):
        if not path in self.images:
            self.images[path] = pygame.image.load(path).convert_alpha()

        return self.images[path]