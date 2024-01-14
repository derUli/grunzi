import os
import random

import pygame
from PygameShader.shader import brightness

from utils.atmosphere.globaleffect import GlobalEffect
from utils.quality import snow_enabled
from constants.quality import QUALITY_LOW, QUALITY_MEDIUM, QUALITY_HIGH

SNOW_COLOR = (255, 255, 255, 0)
SNOW_AMOUNT = 500
SNOW_SPEED = 0.5
SNOW_TEXT = '*'
SNOW_TEXT_SIZE = 24

SNOW_IMAGE_SIZE = (7, 7)


class Snow(GlobalEffect):

    def __init__(self):
        self.enabled = False
        self.snowFall = []
        self.initialized = False
        self.sprites_dir = None

    def start(self, args={}, sprites_dir=None, image_cache=None):
        super().start(args, sprites_dir, image_cache)

        self.snowFall = []
        self.enabled = snow_enabled()

    def init_snow(self, size):

        w, h = size
        for i in range(SNOW_AMOUNT):
            x = random.randrange(0, w)
            y = random.randrange(0, h)
            surface = self.make_surface()
            self.snowFall.append([x, y, surface])

        self.initialized = True

    def make_surface(self):
        quality = QUALITY_LOW  # TODO make it a setting
        surface = None

        if quality >= QUALITY_HIGH:
            surface = self.random_image()
        elif quality >= QUALITY_MEDIUM:
            font = pygame.font.SysFont(None, SNOW_TEXT_SIZE)
            surface = font.render(SNOW_TEXT, True, SNOW_COLOR)
            surface = surface

        return surface

    def random_image(self):
        number = random.randint(1, 6)
        path = os.path.join(self.sprites_dir, 'snow', 'snow' + str(number) + '.png')
        image = self.image_cache.load_image(path, SNOW_IMAGE_SIZE)

        surface = pygame.surface.Surface(image.get_size(), pygame.SRCALPHA | pygame.RLEACCEL)
        surface.blit(image, (0, 0))

        brightness(surface, random.random())
        surface = surface.convert_alpha()
        return surface

    def draw(self, screen):
        if not self.enabled:
            return

        size = screen.get_size()
        w, h = size

        if not self.initialized:
            self.init_snow(screen.get_size())

        for i in range(len(self.snowFall)):
            surface = self.snowFall[i][2]

            if surface:
                screen.blit(surface, self.snowFall[i][:2])
            else:
                pygame.draw.circle(screen, SNOW_COLOR, self.snowFall[i][:2], 2)

            self.snowFall[i][1] += SNOW_SPEED
            if self.snowFall[i][1] > h:
                y = random.randrange(-50, -10)
                self.snowFall[i][1] = y

                x = random.randrange(0, w)
                self.snowFall[i][0] = x
