import os
import random
import time

import pygame
from PygameShader.shader import brightness, greyscale

from constants.quality import QUALITY_MEDIUM, QUALITY_HIGH
from utils.atmosphere.globaleffect import GlobalEffect

RAIN_COLOR = (69, 82, 92)
RAIN_AMOUNT = 500
RAIN_SPEED = 20
RAIN_TEXT = '/'
RAIN_TEXT_SIZE = 30

RAIN_IMAGE_SIZE = (6, 6)

class Rain(GlobalEffect):

    def __init__(self):
        super().__init__()
        self.rain_fall = []
        self.target_count = 0
        self.prefill = False
        self.avg = []

    def start(self, args={}, sprites_dir=None, image_cache=None):
        super().start(args, sprites_dir, image_cache)

        self.rain_fall = []
        self.enabled = True

        self.target_count = 0
        self.prefill = False
        self.font_surface = None

        if 'rain_target_count' in args:
            self.target_count = args['rain_target_count']
            self.prefill = True

        self.target_count = random.randint(100, 500)


    def add_raindrop(self, size):
        start_date = time.time()
        w, h = size
        x = random.randrange(0, w)
        y = random.randrange(0, h)

        surface = self.make_surface()
        self.rain_fall.append([x, y, surface])

        self.avg.append(time.time() - start_date)

    def make_surface(self):
        quality = QUALITY_MEDIUM
        surface = None

        if quality >= QUALITY_HIGH:
            surface = self.random_image()
        elif quality >= QUALITY_MEDIUM:
            if not self.font_surface:
                font = pygame.font.SysFont(None, RAIN_TEXT_SIZE)
                surface = font.render(RAIN_TEXT, True, RAIN_COLOR)
                self.font_surface = surface

            surface = self.font_surface

        return surface

    def random_image(self):
        number = random.randint(1, 6)
        path = os.path.join(self.sprites_dir, 'rain', 'rain' + str(number) + '.png')
        image = self.image_cache.load_image(path, RAIN_IMAGE_SIZE)

        surface = pygame.surface.Surface(image.get_size(), pygame.SRCALPHA | pygame.RLEACCEL)
        surface.blit(image, (0, 0))
        greyscale(surface)
        brightness(surface, random.random())
        return surface

    def draw(self, screen):
        if not self.enabled:
            return

        size = screen.get_size()
        w, h = size

        if self.prefill and len(self.rain_fall) != self.target_count:

            for i in range(self.target_count):
                self.add_raindrop(size)

            self.prefill = False

        if len(self.rain_fall) < self.target_count:
            self.add_raindrop(size)

        for i in range(len(self.rain_fall)):
            surface = self.rain_fall[i][2]

            if surface:
                screen.blit(surface, self.rain_fall[i][:2])
            else:
                pygame.draw.circle(screen, RAIN_COLOR, self.rain_fall[i][:2], 2)

            self.rain_fall[i][1] += RAIN_SPEED

            if self.rain_fall[i][1] > h:
                if len(self.rain_fall) > self.target_count:
                    self.rain_fall[i] = None
                    continue

                y = random.randrange(-50, -10)
                self.rain_fall[i][1] = y

                x = random.randrange(0, w)
                self.rain_fall[i][0] = x

        self.rain_fall = list(filter(lambda item: item is not None, self.rain_fall))

    def to_dict(self):
        return {
            'rain_target_count': self.target_count
        }
