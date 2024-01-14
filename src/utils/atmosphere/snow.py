import random
import pygame

from utils.atmosphere.globaleffect import GlobalEffect
from utils.quality import snow_enabled

SNOW_COLOR = [255, 255, 255]
SNOW_AMOUNT = 50
SNOW_SPEED = 1


class Snow(GlobalEffect):

    def __init__(self):
        self.enabled = False
        self.snowFall = []
        self.initialized = False

    def start(self, args={}, sprites_dir=None, image_cache=None):
        self.enabled = snow_enabled()

    def init_snow(self, size):
        w, h = size
        for i in range(SNOW_AMOUNT):
            x = random.randrange(0, w)
            y = random.randrange(0, h)
            self.snowFall.append([x, y])

        self.initialized = True


    def draw(self, screen):
        if not self.enabled:
            return

        size = screen.get_size()
        w, h = size

        if not self.initialized:
            self.init_snow(screen.get_size())

        for i in range(len(self.snowFall)):
            pygame.draw.circle(screen, SNOW_COLOR, self.snowFall[i], 2)

            self.snowFall[i][1] += SNOW_SPEED
            if self.snowFall[i][1] > h:
                y = random.randrange(-50, -10)
                self.snowFall[i][1] = y

                x = random.randrange(0, w)
                self.snowFall[i][0] = x