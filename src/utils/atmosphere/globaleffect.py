import time
import pygame
from utils.quality import daynightcycle_enabled, bloom_enabled

from PygameShader.shader import zoom, shader_bloom_fast1


class GlobalEffect:

    def __init__(self):
        pass

    def start(self, args={}):
        pass

    def reset(self):
        pass

    def draw(self, screen):
        pass

    def to_dict(self):
        return {}
