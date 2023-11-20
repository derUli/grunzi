""" Gamve Over Screen """
import os
from components.loading_screen import LoadingScreen
from utils.render_cache import store_render, load_render
from utils.string import label_value
from utils.quality import scale_method
import constants.gamepad as gamepad
from constants.headup import BOTTOM_UI_BACKGROUND
from constants import keyboard
from components.maingame import MainGame
from components.fadeable_component import FadeableComponent
from constants.game import MONOTYPE_FONT, LARGE_FONT_SIZE
import pygame
from pygame.surfarray import pixels3d
from PygameShader import tunnel_modeling24, tunnel_render24,\
    zoom, scroll24_inplace, blend_inplace
from PygameShader.BlendFlags import blend_add_surface
import numpy
import math
from math import floor
import logging
import time
FPS = 30

# Seconds
FADEOUT_DURATION = 5

class Intro(FadeableComponent, LoadingScreen):
    """ To be continued Screen """

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.menu = None
        self.cached = []
        self.monotype_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', MONOTYPE_FONT),
            LARGE_FONT_SIZE)

        self.w, self.h = 0, 0
        self.base_surface = None
        self.white_surface = None
        self.faded_out = False
        self.anim = None

        self.fade_speed = 1000 / FPS / 10
        self.fade_begin = 15 * FPS

        self.clock = pygame.time.Clock()
        self.scale = scale_method()
        self.backdrops = []
        self.fps_counter = []
        self.scale_factor = None
        self.prerender_started = time.time()

    def mount(self):
        self.scale_factor = 1.0

        pygame.mouse.set_visible(0)
        pygame.mixer.music.stop()

        self.anim = load_render(
            'intro',
            refresh_interval=FPS/1000,
            loop=False
        )

        if not self.anim:
            self.init()
        else:
            music_file = os.path.join(self.data_dir, 'music', 'intro.ogg')
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play()

    def init(self):
        w, h = self.settings_state.screen_resolution
        w, h = min(w, h), min(w, h)
        w, h = round(w * self.scale_factor), round(h * self.scale_factor)

        self.w = w
        self.h = h

        intro_dir = os.path.join(self.data_dir, 'images', 'intro')

        size = (self.w, self.h)

        self.backdrops = [
            self.image_cache.load_image(os.path.join(intro_dir, 'Bokeh.jpg'), size),
            self.image_cache.load_image(os.path.join(intro_dir, 'space1.jpg'), size),
            self.image_cache.load_image(os.path.join(intro_dir, 'space2.jpg'), size),
            self.image_cache.load_image(os.path.join(intro_dir, 'space1_alpha.jpg'), size)
        ]

        blend_add_surface(self.backdrops[2], self.backdrops[2])

        self.distances, self.angles, self.shades, self.scr_data = tunnel_modeling24(self.w, self.h, self.backdrops[3])
        self.dest_array = numpy.empty((self.w * self.h * 4), numpy.uint8)

        self.acceleration = 1.0
        self.dc = 0.02
        self.df = 1
        self.zx = 0
        self.frame = 0

        self.prev_centerx = 400 + floor((400 >> 1) * math.sin(0 * self.acceleration * 0.25))
        self.prev_centery = 400 + floor((400 >> 1) * math.sin(0 * self.acceleration * 0.5))

        self.base_surface = pygame.surface.Surface((self.w, self.h)).convert(32, pygame.RLEACCEL)
        self.white_surface = pygame.surface.Surface((self.w, self.h), pygame.SRCALPHA | pygame.RLEACCEL).convert()
        self.white_surface.fill(BOTTOM_UI_BACKGROUND)

    def draw(self, screen):
        if self.anim:
            frame = self.anim.get_frame()
            screen.blit(frame,(0,0))

            if not self.anim.has_more_frames():
                self.start_game()
            return

        surface = self.base_surface

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

        if self.alpha > 0:
            self.white_surface.set_alpha(self.alpha)
            surface.blit(self.white_surface, (0,0))

        save_surface = self.scale(surface.copy(), self.screen.get_size())
        self.cached.append(save_surface)

        self.loading_screen(percentage=self.calculate_render_percentage(), loading_text=_('Prerendering sequence...'))

        self.frame += self.df
        self.acceleration += self.dc

        if self.acceleration > 100:
            self.acceleration = 100

        if self.acceleration < 1:
            self.dc *= -1

        if self.frame <= 0:
            self.df *= -1

        self.prev_centerx = centerx
        self.prev_centery = centery

        self.fade()

        if self.alpha >= 255:
            self.faded_out = True

            store_render('intro', self.cached, self.loading_screen)
            prerender_end = time.time() - self.prerender_started
            logging.debug(label_value('Intro sequence prerendered in ', prerender_end))
            self.cached = []
            self.mount()

        if not self.do_fade and self.frame >= self.fade_begin and not self.faded_out:
            self.fadein()

        self.clock.tick(FPS)

        fps = self.clock.get_fps()
        if fps > 0:
            self.fps_counter.append(fps)

    def calculate_render_percentage(self):
        if self.frame == 0:
            return 0

        total_seconds = 18
        total_frames = FPS * total_seconds
        one_percent = 100 / total_frames

        percentage = self.frame * one_percent
        if percentage > 100:
            percentage = 100

        return percentage


    def handle_event(self, event):
        """ Handle events """
        if event.type == pygame.KEYDOWN and event.key in keyboard.CONFIRM_KEYS:
            self.start_game()
        elif event.type == pygame.JOYBUTTONDOWN and event.button == gamepad.K_CONFIRM:
            self.start_game()

    def start_game(self):
        self.screen.fill(BOTTOM_UI_BACKGROUND)
        pygame.display.update()

        component = self.handle_change_component(MainGame)
        component.new_game()

    def handle_exit(self):
        """ Back to main menu"""
        self.handle_change_component(None)
