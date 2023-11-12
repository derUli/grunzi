""" Backdrop sprite """

import math
import sprites.sprite
import time
from utils.quality import scale_method, shader_enabled
from threading import Thread
import logging
from PygameShader.shader import wave

class Water(sprites.sprite.Sprite):
    """ Backdrop sprite """

    def __init__(self, sprite_dir, cache, sprite='water.jpg'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.walkable = False
        self.original_sprite = self.sprite.copy().convert()

        self.angle = 0
        self.loaded = False

        self.update_interval = (1 / 10)
        self.last_update = 0
    def draw(self, screen, x, y):
        pos = self.calculate_pos(x, y)

        if not shader_enabled():
            super().draw(screen, x, y)
            return

        if not self.loaded:
            thread = Thread(target=self.generate_frames_async)
            thread.start()

        frame = self.cache.get_processed_image(self.cache_id(self.angle))

        if not frame:
            return

        screen.blit(frame, pos)

        if time.time() - self.last_update < self.update_interval:
            return

        next_angle = self.angle + 5
        next_angle = next_angle % 360

        if self.cache.get_processed_image(self.cache_id(next_angle)):
            self.last_update = time.time()
            self.angle = next_angle

    def generate_frames_async(self):
        self.loaded = True

        start_time = time.time()

        angle = 0
        while angle <= 360:
            if not self.cache.get_processed_image(self.cache_id(angle)):
                self.cache.add_processed_image(self.cache_id(angle), self.next_frame(angle))

            angle += 5

        end_time = time.time() - start_time
        logging.debug('Waves generated in ' + str(end_time))


    def cache_id(self, angle):
        return 'water-' + str(angle)


    def next_frame(self, angle):
        sprite = self.original_sprite.copy()

        w, h = sprite.get_size()

        wave(sprite, angle * math.pi / 180.0, 12)
        sprite = scale_method()(sprite, (w + 90, h + 90))

        sprite = sprite.convert()

        return sprite
