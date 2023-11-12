""" Backdrop sprite """

import math
import sprites.sprite
from PygameShader.shader import wave
import time
from utils.quality import scale_method, shader_enabled

class Water(sprites.sprite.Sprite):
    """ Backdrop sprite """

    def __init__(self, sprite_dir, cache, sprite='water.jpg'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.walkable = False

        self.angle = 0

        self.update_interval = (1 / 10)
        self.last_update = 0
    def draw(self, screen, x, y):

        if not shader_enabled():
            super().draw(screen, x, y)
            return

        sprite = self.sprite.copy().convert()
        pos = self.calculate_pos(x, y)

        w, h = sprite.get_size()

        wave(sprite, self.angle * math.pi / 180.0, 12)
        sprite = scale_method()(sprite, (w + 90, h + 90))
        screen.blit(sprite, pos)

        if time.time() - self.last_update < self.update_interval:
            return

        self.last_update = time.time()
        self.angle += 5
        self.angle %= 360
