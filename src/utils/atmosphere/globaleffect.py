import time
import pygame
from utils.quality import daynightcycle_enabled, bloom_enabled

from PygameShader.shader import zoom, shader_bloom_fast1


class GlobalEffect:

    def __init__(self):
        self.sprites_dir = None
        self.image_cache = None
        pass

    def start(self, args={}, sprites_dir = None, image_cache = None):
        self.sprites_dir = sprites_dir
        self.image_cache = image_cache
        pass

    def reset(self):
        pass

    def draw(self, screen):
        pass

    def to_dict(self):
        return {}
