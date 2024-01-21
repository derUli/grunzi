""" Toxic sprite """
import random

from constants.direction import DIRECTION_DOWN
from constants.graphics import SPRITE_SIZE
from sprites.sprite import Sprite
from utils.quality import shader_enabled, scale_method

PARTICLE_COUNT = 10
PARTICLE_COLOR = (81, 231, 14, 255)
PARTICLE_RADIUS = 2
PARTICLES_SPEED = 0.5


class Fly(Sprite):
    """ Toxic sprite """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'fly.png')

        self.walkable = False
        self.direction = DIRECTION_DOWN
        self.offset_y = 0
        self.particles = []

        scale_fn = scale_method()
        w, h = 10, 10

        self.sprite = scale_fn(self.sprite, (w, h))

    def randomize(self):
        w, h = SPRITE_SIZE

        while len(self.particles) < PARTICLE_COUNT:
            x = random.randint(PARTICLE_RADIUS, w - PARTICLE_RADIUS)
            y = random.randint(PARTICLE_RADIUS, h - PARTICLE_RADIUS)

            particle = [x, y]

            self.particles.append(particle)

    def draw(self, screen, x, y):
        """ draw sprite """

        if not shader_enabled():
            return

        if len(self.particles) == 0:
            self.randomize()

        x, y = self.calculate_pos(x, y)
        w, h = SPRITE_SIZE
        w -= self.sprite.get_width()
        h -= self.sprite.get_height()

        for i in range(len(self.particles)):
            particle = self.particles[i]
            draw_pos = (
                x + particle[0],
                y + particle[1]
            )

            screen.blit(self.sprite, draw_pos)

            particle[0] += random.randint(-1, 1)
            if particle[0] != 0:
                particle[1] += random.randint(-1, 1)

            if particle[0] < 0:
                particle[0] = 0

            if particle[0] > w:
                particle[0] = w

            if particle[1] < 0:
                particle[1] = 0

            if particle[1] > h:
                particle[1] = h

            self.particles[i] = particle
