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


class Fog(GlobalEffect):

    def __init__(self):
        self.enabled = False
        self.cache = ImageCache()

    def reset(self):
        # Not implemented yet
        self.enabled = False

    def draw(self, screen):
        if not self.enabled:
            return

        screen.fill((255, 255, 255))
