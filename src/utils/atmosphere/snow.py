import os
import random
import time
import pygame
from PygameShader.shader import brightness, greyscale
from utils.atmosphere.globaleffect import GlobalEffect
from utils.quality import snow_enabled, snow_quality
from constants.quality import QUALITY_MEDIUM, QUALITY_HIGH

SNOW_COLOR = (255, 255, 255, 0)
SNOW_AMOUNT = 500
SNOW_SPEED = 0.5
SNOW_TEXT = '*'
SNOW_TEXT_SIZE = 24

SNOW_IMAGE_SIZE = (6, 6)


class Snow(GlobalEffect):

    def __init__(self):
        super().__init__()
        self.snow_fall = []
        self.target_count = 0
        self.prefill = False
        self.avg = []

    def start(self, args={}, sprites_dir=None, image_cache=None):
        super().start(args, sprites_dir, image_cache)

        self.snow_fall = []
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
        self.snow_fall.append([x, y, surface])
        
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
        
        if self.prefill and len(self.snow_fall) != self.target_count:
            
            for i in range(self.target_count):
                self.add_snowflake(size)
            
            self.prefill = False

        if len(self.snow_fall) < self.target_count:
            self.add_snowflake(size)

        for i in range(len(self.snow_fall)):
            surface = self.snow_fall[i][2]

            if surface:
                screen.blit(surface, self.snow_fall[i][:2])
            else:
                pygame.draw.circle(screen, SNOW_COLOR, self.snow_fall[i][:2], 2)

            self.snow_fall[i][1] += SNOW_SPEED
            
            if self.snow_fall[i][1] > h:
                if len(self.snow_fall) > self.target_count:
                    self.snow_fall[i] = None
                    continue

                y = random.randrange(-50, -10)
                self.snow_fall[i][1] = y

                x = random.randrange(0, w)
                self.snow_fall[i][0] = x

        self.snow_fall = list(filter(lambda item: item is not None, self.snow_fall))

    def to_dict(self):
        return {
            'snow_target_count': self.target_count
        }