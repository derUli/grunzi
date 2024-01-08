import time
import pygame
from utils.quality import daynightcycle_enabled, bloom_enabled
from utils.atmosphere.globaleffect import GlobalEffect
from PygameShader.shader import zoom, shader_bloom_fast1
from utils.image import ImageCache


UPDATE_DATETIME_INTERVAL = 1.1765  # Halber Tag in Spielzeit = 300 Sekunden
DARKEST_DAYTIME = 240
BRIGHTEST_DAYTIME = 0

DEFAULT_DAYTIME = 20
MODIFIER_DARK = 1
MODIFIER_LIGHT = -1

RAIN_CHAR = '/'
RAIN_COLOR = (100, 100, 100)


class Rain(GlobalEffect):

    def __init__(self):
        self.enabled = False
        self.cache = ImageCache()

        self.font = pygame.font.SysFont(None, 12, bold=True)
        self.drop = None
        self.threshold = 10

    def reset(self):
        # Not implemented yet
        self.enabled = False

    def draw(self, screen):
        if not self.enabled:
            return

        if not self.drop:
            self.drop = self.craete_drop

    def add_drop(self, screen):

        w, h = screen.get_size()

    def craete_drop(self):
        return self.font.render(RAIN_CHAR, True, RAIN_COLOR)
