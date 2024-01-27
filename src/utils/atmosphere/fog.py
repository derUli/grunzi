import os
import time
from time import time

import pygame

from utils.atmosphere import ATMOSPHERE_FOG
from utils.atmosphere.globaleffect import GlobalEffect
from utils.quality import fog_enabled

UPDATE_DATETIME_INTERVAL = 1.1765  # Halber Tag in Spielzeit = 300 Sekunden
DARKEST_DAYTIME = 240
BRIGHTEST_DAYTIME = 0

DEFAULT_DAYTIME = 20
MODIFIER_DARK = 1
MODIFIER_LIGHT = -1

FOG_ALPHA_SPEED = 0.5
FOG_MOVE_SPEED = 1 / 10


class Fog(GlobalEffect):

    def __init__(self):
        self.fog = []
        self.alpha = 0
        self.target_alpha = 0
        self.last_updated = time()
        self.id = ATMOSPHERE_FOG

    def start(self, args={}, sprites_dir=None, image_cache=None):
        super().start(args, sprites_dir, image_cache)

        if 'fog_alpha' in args:
            self.alpha = args['fog_alpha']

        if 'fog_target_alpha' in args:
            self.target_alpha = args['fog_target_alpha']

    def reset(self):
        self.enabled = fog_enabled()
        self.fog = []
        self.alpha = 0
        self.target_alpha = 0

        self.buffer = None

    def draw(self, screen):
        if not self.enabled:
            return

        if self.alpha == 0 and self.target_alpha == 0:
            return

        if len(self.fog) == 0:
            self.init_fog(screen.get_size())

        if self.alpha < self.target_alpha:
            self.alpha += FOG_ALPHA_SPEED
        elif self.alpha > self.target_alpha:
            self.alpha -= FOG_ALPHA_SPEED

        if time() < self.last_updated + FOG_MOVE_SPEED and self.buffer:
            self.buffer.set_alpha(int(self.alpha))
            screen.blit(self.buffer, (0, 0))
            return

        self.buffer = pygame.surface.Surface(
            screen.get_size(), pygame.SRCALPHA)

        for fog in self.fog:

            w = fog['image'].get_width()
            x, y = fog['pos']

            self.last_updated = time()
            x -= 1

            if x <= w * -1:
                x = w

            if self.alpha > 0:
                self.buffer.blit(fog['image'], (x, y))

            fog['pos'] = (x, y)

        self.buffer.set_alpha(int(self.alpha))
        screen.blit(self.buffer, (0, 0))

    def to_dict(self):
        return {
            'fog_alpha': self.alpha,
            'fog_target_alpha': self.target_alpha
        }

    def init_fog(self, size):
        file = os.path.join(self.sprites_dir, 'backdrops', 'fog.png')
        image_left = self.image_cache.load_image(file, size)
        image_right = pygame.transform.flip(
            image_left, flip_x=True, flip_y=False)

        self.fog = [
            {
                'pos': (0, 0),
                'image': image_left
            },
            {
                'pos': (image_right.get_width(), 0),
                'image': image_right
            }
        ]

    def update(self, alpha):
        self.target_alpha = alpha
