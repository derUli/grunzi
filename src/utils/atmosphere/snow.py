import os
import random
import time
import pygame
from PygameShader.shader import brightness, greyscale
import numpy
from utils.atmosphere.globaleffect import GlobalEffect
from utils.quality import snow_enabled, snow_quality
from constants.quality import QUALITY_LOW, QUALITY_MEDIUM, QUALITY_HIGH

SNOW_COLOR = (255, 255, 255, 0)
SNOW_AMOUNT = 500
SNOW_SPEED = 0.5
SNOW_TEXT = '*'
SNOW_TEXT_SIZE = 24

SNOW_IMAGE_SIZE = (6, 6)


class Snow(GlobalEffect):

    def __init__(self):
        self.enabled = False
        self.snowFall = []
        self.sprites_dir = None
        self.target_count = 0
        self.prefill = False
        self.avg = []

    def start(self, args={}, sprites_dir=None, image_cache=None):
        super().start(args, sprites_dir, image_cache)

        self.snowFall = []
        self.enabled = snow_enabled()

        self.target_count = 0
        self.prefill = False
        self.font_surface = None

        if 'snow_target_count' in args:
            self.target_count = args['snow_target_count']
            self.prefill = True

    def add_snowflake(self, size):
        start_date = time.time()
        w, h = size
        x = random.randrange(0, w)
        y = random.randrange(0, h)
        
        surface = self.make_surface()
        self.snowFall.append([x, y, surface])
        
        self.avg.append(time.time() - start_date)

    def make_surface(self):
        quality = snow_quality()
        surface = None

        if quality >= QUALITY_HIGH:
            surface = self.random_image()
        elif quality >= QUALITY_MEDIUM:
            if not self.font_surface:
                font = pygame.font.SysFont(None, SNOW_TEXT_SIZE)
                surface = font.render(SNOW_TEXT, True, SNOW_COLOR)
                self.font_surface = surface

            surface = self.font_surface

        return surface

    def random_image(self):
        number = random.randint(1, 6)
        path = os.path.join(self.sprites_dir, 'snow', 'snow' + str(number) + '.png')
        image = self.image_cache.load_image(path, SNOW_IMAGE_SIZE)

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
        
        if self.prefill and len(self.snowFall) != self.target_count:
            
            for i in range(self.target_count):
                self.add_snowflake(size)
            
            self.prefill = False

        if len(self.snowFall) < self.target_count:
            self.add_snowflake(size)

        for i in range(len(self.snowFall)):
            surface = self.snowFall[i][2]

            if surface:
                screen.blit(surface, self.snowFall[i][:2])
            else:
                pygame.draw.circle(screen, SNOW_COLOR, self.snowFall[i][:2], 2)

            self.snowFall[i][1] += SNOW_SPEED
            
            if self.snowFall[i][1] > h:
                if len(self.snowFall) > self.target_count:
                    self.snowFall[i] = None
                    continue

                y = random.randrange(-50, -10)
                self.snowFall[i][1] = y

                x = random.randrange(0, w)
                self.snowFall[i][0] = x

        self.snowFall = list(filter(lambda item: item is not None, self.snowFall))

    def to_dict(self):
        return {
            'snow_target_count': self.target_count
        }