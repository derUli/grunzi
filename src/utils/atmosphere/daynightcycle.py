import time

import pygame
from PygameShader.shader import shader_bloom_fast1

from utils.atmosphere.globaleffect import GlobalEffect
from utils.quality import daynightcycle_enabled, bloom_enabled

UPDATE_DATETIME_INTERVAL = 1.1765  # Halber Tag in Spielzeit = 300 Sekunden
DARKEST_DAYTIME = 240
BRIGHTEST_DAYTIME = 0

DEFAULT_DAYTIME = 0
MODIFIER_DARK = 1
MODIFIER_LIGHT = -1


class DayNightCycle(GlobalEffect):

    def __init__(self):
        self.daytime = 0
        self.daytime_updated = time.time()
        self.modifier = MODIFIER_DARK
        self.surfaces = None
        self.enabled = False

    def start(self, args={}, sprites_dir=None, image_cache=None):
        super().start(args, sprites_dir, image_cache)

        if 'dnc_daytime' in args:
            self.daytime = args['dnc_daytime']

        if 'dnc_modifier' in args:
            self.modifier = args['dnc_modifier']

    def to_dict(self):
        return {
            'dnc_daytime': self.daytime,
            'dnc_modifier': self.modifier
        }

    def reset(self):
        self.daytime = DEFAULT_DAYTIME
        self.daytime_updated = time.time()
        self.surface = None
        self.enabled = daynightcycle_enabled()
        self.modifier = MODIFIER_DARK
        self.surfaces = None

    def init_surface(self, screen):
        w, h = screen.get_size()
        self.surface = pygame.surface.Surface(
            (w, h), pygame.SRCALPHA | pygame.RLEACCEL).convert_alpha()

        self.surface.fill((0, 0, 0))

    def draw(self, screen):
        if not self.enabled:
            return

        if not self.surface:
            self.init_surface(screen)
            self.surface.set_alpha(self.daytime)

        # Todo: Split drawing and updating
        if time.time() - self.daytime_updated >= UPDATE_DATETIME_INTERVAL:
            self.daytime_updated = time.time()
            self.daytime += self.modifier
            self.surface.set_alpha(self.daytime)

            if self.daytime >= DARKEST_DAYTIME:
                self.modifier = MODIFIER_LIGHT
            elif self.daytime <= BRIGHTEST_DAYTIME:
                self.modifier = MODIFIER_DARK

        if self.daytime > 0:
            self.surface.set_alpha(self.daytime)
            screen.blit((self.surface), (0, 0))

        if not bloom_enabled():
            return

        bloom_amount = 127.5 + self.daytime

        if bloom_amount < 255:
            shader_bloom_fast1(screen, bloom_amount)
