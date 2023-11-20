""" Guitar sprite """
import pygame.surface
from sprites.coin import Coin
from utils.quality import font_antialiasing_enabled
from sprites.sprite import Sprite
import random
import os
import logging
try:
    from PygameShader.shader_gpu import block_grid, get_gpu_info, zoom_gpu, bloom_gpu
except ImportError as e:
    logging.error(e)
    zoom_gpu = None
    bloom_gpu = None


from PygameShader.shader import zoom, shader_bloom_fast1

from pygame.math import Vector2
from utils.quality import scale_method
TEXT_POS = (830, 50)
FONT_SIZE = 24
TEXT_COLOR=(0,0,0)
SCALE_SPEED = 0.005
SCALE_FROM = 0.9999
SCALE_TO = 0.5

TEXT_FONT='adrip1.ttf'
class Telescope(Sprite):
    """ Guitar sprite class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'telescope.png')
        self.sound = None
        code = [1, 2, 3, 4]
        random.shuffle(code)
        self.screen = None

        self.attributes = {
            'code': code,
            'unlocked': False
        }
        self.backdrop = pygame.image.load(
            os.path.join(self.sprite_dir, 'backdrops', 'mountainside.jpg')
        ).convert()

        self.scopes = pygame.image.load(
            os.path.join(self.sprite_dir, '..', 'ui', 'scopes.png')
        ).convert_alpha()

        # TODO: Replace with a better fitting font
        self.font = pygame.font.Font(
            os.path.join(self.sprite_dir, '..', '..', 'fonts', TEXT_FONT),
            FONT_SIZE
        )
        self.base_surface = None
        self.player_state = None
        self.viewport_x = 0
        self.viewport_y = 0
        self.scale_z = SCALE_FROM
        self.scale = scale_method()
        self.cached = {}

        self.grid = None
        self.block = None


    def draw(self, screen, x, y):
        self.screen = screen
        if self.player_state and self.player_state.show_detailed:
            self.player_state.show_detailed = self.draw_telescope_view(self.screen)
            return

        super().draw(screen, x, y)

    def draw_telescope_view(self, screen):
        if not self.base_surface:
            self.base_surface = pygame.surface.Surface(self.backdrop.get_size())

            self.base_surface.blit(self.backdrop, (0,0))

            text = self.font.render(
                "".join(map(str, self.attributes['code'])),
                font_antialiasing_enabled(),
                TEXT_COLOR

            )
            self.base_surface.blit(text, TEXT_POS)

        w, h = self.base_surface.get_size()

        MOUSE_POS = Vector2(pygame.mouse.get_pos())
        if MOUSE_POS.x < 0: MOUSE_POS.x = 0
        if MOUSE_POS.x > w: MOUSE_POS.x = w
        if MOUSE_POS.y < 0: MOUSE_POS.y = 0
        if MOUSE_POS.y > h: MOUSE_POS.y = h

        cache_id = (MOUSE_POS.x, MOUSE_POS.y, self.scale_z)

        if cache_id in self.cached:
            return self.cached[cache_id]

        if callable(zoom_gpu):
            if not self.grid:
                self.grid, self.block = block_grid(self.screen.get_width(), self.screen.get_height())
            surf = zoom_gpu(self.base_surface, MOUSE_POS.x, MOUSE_POS.y, self.grid, self.block, self.scale_z)
        else:
            surf = zoom(self.base_surface, MOUSE_POS.x, MOUSE_POS.y, self.scale_z)

        if self.scale_z >= SCALE_TO:
            self.scale_z -= SCALE_SPEED

        if self.scopes.get_size() != self.screen.get_size():
            self.scopes = self.scale(self.scopes, self.screen.get_size())

        if MOUSE_POS.y < 255:
            if callable(bloom_gpu):
                surf = bloom_gpu(surf, threshold_=MOUSE_POS.y)
            else:
                shader_bloom_fast1(surf, threshold_=MOUSE_POS.y)

        surf.blit(self.scopes, (0,0))

        # self.cached[cache_id] = surf

        return surf

    def handle_interact(self, element):
        unlocked = 'unlocked' in self.attributes and self.attributes['unlocked']
        if not unlocked:
            element.state.say(_('[Insert Coin]'))
            return

        self.player_state = element.state
        self.player_state.show_detailed = self.draw_telescope_view(self.screen)

        element.state.say(_('Move mouse to look'))


    def handle_interact_item(self, element):
        # Activate the telescope with a coin
        if not element:
            return

        if isinstance(element.state.inventory, Coin):
            self.attributes['unlocked'] = True
            element.state.use_item = False
            element.state.inventory = None
