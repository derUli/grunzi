import time
import os
import pygame
from utils.quality import fog_enabled
from utils.atmosphere.globaleffect import GlobalEffect
from PygameShader.shader import zoom, shader_bloom_fast1
from utils.image import ImageCache


UPDATE_DATETIME_INTERVAL = 1.1765  # Halber Tag in Spielzeit = 300 Sekunden
DARKEST_DAYTIME = 240
BRIGHTEST_DAYTIME = 0

DEFAULT_DAYTIME = 20
MODIFIER_DARK = 1
MODIFIER_LIGHT = -1

FOG_ALPHA_SPEED = 0.5
FOG_MOVE_SPEED = 0.1

class Fog(GlobalEffect):

    def __init__(self):
        self.enabled = False
        self.fog = []
        self.alpha = 0
        self.target_alpha = 0

    def start(self, args={}, sprites_dir = None, image_cache = None):
        super().start(args, sprites_dir, image_cache)

        if 'fog_alpha' in args:
            self.alpha = args['fog_alpha']
        
        if 'fog_target_alpha' in args:
            self.target_alpha = args['fog_target_alpha']


    def reset(self):
        # Not implemented yet
        self.enabled = fog_enabled()
        self.fog = []
        self.alpha = 0
        self.target_alpha = 255

    def draw(self, screen):
        if not self.enabled:
            return

        if len(self.fog) == 0:
            self.init_fog(screen.get_size())

        if self.alpha < self.target_alpha:
            self.alpha += FOG_ALPHA_SPEED
        elif self.alpha > self.target_alpha:
            self.alpha -= FOG_ALPHA_SPEED


        for fog in self.fog:
            
            x, y = fog['pos']

            if self.alpha > 0:
                fog['image'].set_alpha(int(self.alpha))
                screen.blit(fog['image'], (int(x), y))

            x -= FOG_MOVE_SPEED

            w = fog['image'].get_width()

            if x <= w * -1:
                x = w + 1

            fog['pos'] = (x, y)


    def to_dict(self):
        return {
            'fog_alpha': self.alpha,
            'fog_target_alpha': self.target_alpha
        }


    def init_fog(self, size):
        file = os.path.join(self.sprites_dir, 'backdrops', 'fog.png')
        image_left = self.image_cache.load_image(file, size)
        image_right = pygame.transform.flip(image_left, flip_x = True, flip_y = False)

        self.fog = [
            {
                'pos': (0, 0),
                'image': image_left
            },
            {
                'pos': (image_right.get_width() + 1, 0),
                'image': image_right
            }
        ]
