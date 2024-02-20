import os
import time

import pygame

from constants.game import LARGE_FONT_SIZE, REGULAR_FONT
from constants.headup import UI_MARGIN, BOTTOM_UI_BACKGROUND
from utils.atmosphere.globaleffect import GlobalEffect
from utils.quality import font_antialiasing_enabled

PHASE_SLIDE_IN = 1
PHASE_WAIT = 2
PHASE_SLIDE_OUT = 3

TEXT_COLOR = (255, 255, 255)


class Notification(GlobalEffect):

    def __init__(self):
        super().__init__()
        self.message = None
        self.box = None

        self.x = UI_MARGIN
        self.target_x = UI_MARGIN
        self.y = UI_MARGIN

        self.screen = None
        self.phase = None
        self.font = None
        self.wait_to = None

    def start(self, args={}, sprites_dir=None, image_cache=None):
        super().start(args, sprites_dir, image_cache)

        fontfile = os.path.join(sprites_dir, '..', '..', 'fonts', REGULAR_FONT)
        self.font = pygame.font.Font(
            fontfile,
            LARGE_FONT_SIZE
        )

        self.phase = None

    def draw(self, screen):
        self.screen = screen

        if not self.box:
            return

        if not self.phase:
            return

        if self.phase == PHASE_SLIDE_IN:
            self.x += 1
            if self.x >= self.target_x:
                self.phase = PHASE_WAIT
                self.wait_to = time.time() + 5
        elif self.phase == PHASE_WAIT and time.time() > self.wait_to:
            self.phase = PHASE_SLIDE_OUT
            self.target_x = 0 - self.box.get_width()
        elif self.phase == PHASE_SLIDE_OUT:
            self.x -= 1

            if self.x < self.target_x:
                self.box = None
                self.phase = None
                return

        screen.blit(self.box, (self.x, self.y))

    def update(self, message):
        self.message = message

        rendered_text = self.font.render(
            self.message,
            font_antialiasing_enabled(),
            TEXT_COLOR
        )

        w, h = rendered_text.get_size()

        w += UI_MARGIN * 2
        h += UI_MARGIN * 2

        x = w / 2 - rendered_text.get_width() / 2
        y = h / 2 - rendered_text.get_height() / 2

        self.box = pygame.surface.Surface((w, h))
        self.box.fill(BOTTOM_UI_BACKGROUND)
        self.box.blit(rendered_text, (x, y))

        self.x = 0 - self.box.get_width()
        self.target_x = UI_MARGIN
        self.phase = PHASE_SLIDE_IN
