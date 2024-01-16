""" Toxic sprite """
import random

import pygame.draw

from constants.direction import DIRECTION_DOWN
from constants.graphics import SPRITE_SIZE
from sprites.sprite import Sprite
from utils.quality import shader_enabled

PARTICLE_COUNT = 10
PARTICLE_COLOR = (81, 231, 14, 255)
PARTICLE_RADIUS = 2
PARTICLES_SPEED = 0.5
HURT_DAMAGE = 10

class Toxic(Sprite):
    """ Toxic sprite """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
        super().__init__(sprite_dir, cache, 'placeholder.png')

        self.walkable = False
        self.direction = DIRECTION_DOWN
        self.offset_y = 0
        self.particles = []

    def randomize(self):
        w, h = SPRITE_SIZE

        while len(self.particles) < PARTICLE_COUNT:
            x = random.randint(1, w - 1)
            y = random.randint(1, h - 1)

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

        for i in range(len(self.particles)):
            particle = self.particles[i]
            draw_pos = (
                x + particle[0],
                y + particle[1]
            )
            rect = pygame.draw.circle(screen, PARTICLE_COLOR, draw_pos, PARTICLE_RADIUS)
            particle[1] -= PARTICLES_SPEED

            if particle[1] <= rect.h:
                particle[0] = random.randint(1, w - 1)
                particle[1] = h - 1
                self.particles[i] = particle

    def handle_interact(self, element):
        if not element:
            return

        element.state.hurt(HURT_DAMAGE)