import random
import os
import pygame

from utils.atmosphere.globaleffect import GlobalEffect
from utils.quality import snow_enabled
from PygameShader.shader import greyscale, brightness

SNOW_COLOR = (255, 255, 255, 0)
SNOW_AMOUNT = 500
SNOW_SPEED = 0.5
SNOW_TEXT = '*'
SNOW_IMAGE_SIZE = (6, 6)

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
        surface = None
        font = pygame.font.SysFont(None, 24)
        #surface = font.render(SNOW_TEXT, True, SNOW_COLOR)

        w, h = size
        for i in range(SNOW_AMOUNT):
            x = random.randrange(0, w)
            y = random.randrange(0, h)
            surface = self.random_image()
            self.snowFall.append([x, y, surface])

        self.initialized = True


    def random_image(self):
        number = random.randint(1, 6)
        path = os.path.join(self.sprites_dir, 'snow', 'snow' + str(number) + '.png')
        image = self.image_cache.load_image(path, SNOW_IMAGE_SIZE).copy()
        # greyscale(image)
        brightness(image, random.random())
        return image

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
