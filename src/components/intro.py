""" Gamve Over Screen """
import os

from utils.quality import scale_method
from constants.quality import QUALITY_LOW, QUALITY_MEDIUM, QUALITY_VERY_HIGH, QUALITY_VERY_LOW
from constants import gamepad
from constants import keyboard
from components.maingame import MainGame
from components.fadeable_component import FadeableComponent
from constants.game import MONOTYPE_FONT, LARGE_FONT_SIZE
import pygame
from pygame.surfarray import pixels3d
from PygameShader import tunnel_modeling24, tunnel_render24,\
    zoom, scroll24_inplace, blend_inplace, blur
from PygameShader.BlendFlags import blend_add_surface
import numpy
import math
from math import floor

class Intro(FadeableComponent):
    """ To be continued Screen """

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.menu = None

        self.monotype_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', MONOTYPE_FONT),
            LARGE_FONT_SIZE)

        self.w, self.h = 0, 0

        self.scale = scale_method()
        self.backdrops = []

    def draw(self, screen):

        surface = pygame.surface.Surface((self.w, self.h))

        centerx = floor((400 >> 1) * math.sin(self.frame * self.acceleration * 0.25))
        centery = floor((400 >> 1) * math.sin(self.frame * self.acceleration * 0.5))
        dx = self.prev_centerx - centerx
        dy = self.prev_centery - centery

        if dx > 0:
            dx = -1
        elif dx < 0:
            dx = 1
        if dy > 0:
            dy = -1
        elif dy < 0:
            dy = 1

        scroll24_inplace(self.backdrops[1], dx, dy)

        surface.blit(self.backdrops[0], (0, 0))

        zx = 0.9999 - (self.frame / float(800.0))
        surf = zoom(self.backdrops[1], 400, 400, max(zx, 0))
        surface.blit(surf, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        percentage = (1 - zx) * 60

        if percentage > 100:
            percentage = 100

        blend_inplace(
            source_=surface,
            destination_=pixels3d(self.backdrops[2]),
            percentage_=percentage
        )

        surface_ = tunnel_render24(
            self.frame * self.acceleration,
            self.w,
            self.h,
            self.w >> 1,
            self.h >> 1,
            self.distances,
            self.angles,
            self.shades,
            self.scr_data,
            self.dest_array
        )

        surface.blit(surface_, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        white = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA)
        white.fill((255,255, 255))
        print(self.alpha)
        white.set_alpha(self.alpha)
        surface.blit(white, (0,0))
        screen.blit(self.scale(surface, screen.get_size()), (0, 0))

        self.frame += self.df
        self.acceleration += self.dc

        if self.acceleration > 100:
            self.dc *= -1
            self.df *= -1

        if self.acceleration < 1:
            self.dc *= -1

        if self.frame <= 0:
            self.df *= -1

        self.prev_centerx = centerx
        self.prev_centery = centery

        music_pos = pygame.mixer.music.get_pos()
        # 23000

        if not self.do_fade and music_pos >= 23000:
            self.fadein()
            return

        print(self.alpha)

        if self.alpha >= 255:
            self.start_game()

        self.fade()



    def mount(self):
        pygame.mouse.set_visible(0)
        w, h = self.settings_state.screen_resolution

        w, h = min(w, h),  min(w, h)

        # Scale factor based on quality settings

        scale_factor = 1.0

        if self.settings_state.quality >= QUALITY_VERY_HIGH:
            scale_factor = 1.1
        elif self.settings_state.quality >= QUALITY_MEDIUM:
            scale_factor = 1.0
        elif self.settings_state.quality >= QUALITY_LOW:
            scale_factor = 0.8
        elif self.settings_state.quality >= QUALITY_VERY_LOW:
            scale_factor = 0.5

        w, h = round(w * scale_factor), round(h * scale_factor)

        self.w = w
        self.h = h

        intro_dir = os.path.join(self.data_dir, 'images', 'intro')

        size = (self.w, self.h)

        self.backdrops = [
            self.image_cache.load_image(os.path.join(intro_dir, 'Bokeh.jpg'), size),
            self.image_cache.load_image(os.path.join(intro_dir, 'space1.jpg'), size),
            self.image_cache.load_image(os.path.join(intro_dir, 'space2.jpg'), size),
            self.image_cache.load_image(os.path.join(intro_dir, 'space1_alpha.jpg'))
        ]

        blend_add_surface(self.backdrops[2], self.backdrops[2])

        self.distances, self.angles, self.shades, self.scr_data = tunnel_modeling24(self.w, self.h, self.backdrops[3])
        self.dest_array = numpy.empty((self.w * self.h * 4), numpy.uint8)

        self.acceleration = 1.0
        self.dc = 0.02
        self.df = 1
        self.zx = 0
        self.frame = 0

        self.prev_centerx = 400 + floor((400 >> 1) * math.sin(0 * self. acceleration * 0.25))
        self.prev_centery = 400 + floor((400 >> 1) * math.sin(0 * self.acceleration * 0.5))

        music_file = os.path.join(self.data_dir, 'music', 'intro.ogg')
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()



    def handle_event(self, event):
        """ Handle events """
        if event.type == pygame.KEYDOWN and event.key in keyboard.CONFIRM_KEYS:
            self.start_game()

    def start_game(self):
        component = self.handle_change_component(MainGame)
        component.new_game()

    def handle_exit(self):
        """ Back to main menu"""
        self.handle_change_component(None)
