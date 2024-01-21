import os
import random
import time

import pygame

import utils.audio
from constants.quality import QUALITY_MEDIUM, QUALITY_HIGH
from utils.atmosphere import ATMOSPHERE_RAIN
from utils.atmosphere.globaleffect import GlobalEffect
from utils.audio import play_sound
from utils.quality import weather_enabled

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
        self.sound = None
        self.sound_file = None
        self.id = ATMOSPHERE_RAIN

    def start(self, args={}, sprites_dir=None, image_cache=None):
        super().start(args, sprites_dir, image_cache)

        self.rain_fall = []
        self.enabled = weather_enabled()

        self.target_count = 0
        self.prefill = False
        self.font_surface = None
        self.sound = None

        if 'rain_target_count' in args:
            self.target_count = args['rain_target_count']
            self.prefill = True

        self.sound = None
        self.sound_file = os.path.join(self.sprites_dir, '..', '..', 'sounds', 'weather', 'rain.ogg')

    def add_raindrop(self, size):
        start_date = time.time()
        w, h = size
        x = random.randrange(0, w)
        y = random.randrange(0, h)

        surface = self.make_surface()
        self.rain_fall.append([x, y, surface])

        self.avg.append(time.time() - start_date)

    def make_surface(self):
        quality = QUALITY_HIGH
        surface = None

        if quality >= QUALITY_MEDIUM:
            if not self.font_surface:
                font = pygame.font.SysFont(None, RAIN_TEXT_SIZE)
                surface = font.render(RAIN_TEXT, True, RAIN_COLOR)
                self.font_surface = surface

            surface = self.font_surface

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

        if any(self.rain_fall):
            if not self.sound:
                self.sound = play_sound(self.sound_file, -1)

            self.sound.unpause()

        elif self.sound and self.sound.get_busy():
            self.sound.pause()

        one_drop_volume = 0.005

        volume = len(self.rain_fall) * one_drop_volume

        if volume > 1:
            volume = 1

        volume = volume * utils.audio.SOUND_VOLUME
        if self.sound:
            self.sound.set_volume(volume)

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

    def set_value(self, target_count):
        self.target_count = target_count

    def to_dict(self):
        return {
            'rain_target_count': self.target_count
        }
