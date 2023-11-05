""" Main character sprite """

import pygame
import logging

import sprites.sprite
from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT


class Character(sprites.sprite.Sprite):
    """ Main character sprite class """

    def __init__(self, sprite_dir, cache, sprite='pig.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction

        self.center_camera = False

        # One tile by second
        self.walk_speed = 0.15
        self.sprint_speed = self.walk_speed * 0.4
        self.last_movement = 0

    def draw(self, screen, x, y):
        """ Draw sprite """
        sprite = self.sprite.copy()

        flip_x = False
        flip_y = False

        if self.image_direction == DIRECTION_LEFT:
            flip_x = True
        sprite = pygame.transform.flip(sprite, flip_x, flip_y)

        pos = self.calculate_pos(x, y)

        screen.blit(sprite, pos)

        return pos

    def ai(self, level):
        # logging.debug(level.search_sprite(self))
        return

    def change_direction(self, direction):
        """ Change sprite direction """
        self.direction = direction
        if direction in [DIRECTION_LEFT, DIRECTION_RIGHT]:
            self.image_direction = direction
