""" Main character sprite """

import pygame

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

        self.walk_speed = 0.11
        self.sprint_speed = self.walk_speed * 0.6
        self.last_movement = 0

    def draw(self, screen, x, y):

        """ Draw sprite """
        sprite = self.sprite.copy()

        flip_x = False
        flip_y = False

        if self.image_direction == DIRECTION_LEFT:
            flip_x = True
        sprite = pygame.transform.flip(sprite, flip_x, flip_y)

        pos_x, pos_y = self.calculate_pos(x, y)

        pos_x += self.mov_offset_x
        pos_y += self.mov_offset_y

        drawn = screen.blit(sprite, (pos_x, pos_y))

        return drawn

    def change_direction(self, direction):
        """ Change sprite direction """
        self.direction = direction
        if direction in [DIRECTION_LEFT, DIRECTION_RIGHT]:
            self.image_direction = direction
