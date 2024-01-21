""" Racoon character """

from PygameShader import fire_effect
import pygame

import sprites.sprite
import numpy

import utils.quality
from constants.graphics import SPRITE_SIZE


class Fire(sprites.sprite.Sprite):
    """ Fire character class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """

        super().__init__(sprite_dir, cache, 'gras1.jpg')

        self.walkable = False

        self.fire_palette = numpy.zeros(255, dtype=numpy.uint)
        self.fire_array = numpy.zeros((100, 100), dtype=numpy.float32)

        self.bpf = 0
        self.delta = +0.1

    def draw(self, screen, x, y):

        w, h = SPRITE_SIZE
        """ Draw current frame of fire animation """
        pos = self.calculate_pos(x, y)

        smooth = False
        bloom = False
        fast_bloom = False
        blur = False

        # Execute the shader fire effect
        frame = fire_effect(
            w,
            h,
            4,
            self.fire_palette,
            self.fire_array,
            fire_intensity_= 16,
            reduce_factor_=4,
            bloom_=bloom,
            fast_bloom_=fast_bloom,
            bpf_threshold_=self.bpf,
            low_=20,
            high_=w,
            blur_=blur,
            smooth_=smooth,
            # surface_=TmpSurface,
            # No need to define a palette pre-processing,
            # the algo will create a new palette with the given
            # hsl_ values
            adjust_palette_=True,
            hsl_=(0.2, 200, 1.8)
        )

        screen.blit(frame, pos, special_flags=pygame.BLEND_RGB_MAX)


        self.bpf += self.delta
        self.bpf = max(self.bpf, 45)
        self.bpf = min(self.bpf, 0)

        if self.bpf == 45:
            self.delta *= -1

    def handle_interact(self, element):
        if element and element.state:
            element.state.hurt(15)

