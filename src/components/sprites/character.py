import constants.graphics
from constants.direction import *
import components.sprites.sprite
import pygame

class Character(components.sprites.sprite.Sprite):
    def __init__(self, sprite_dir, cache, sprite = 'pig.png'):
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction
        self.center_camera = True



    def draw(self, screen, x, y):

        sprite = self.sprite.copy()

        flip_x = False
        flip_y = False

        if(self.image_direction == DIRECTION_LEFT):
            flip_x = True

        sprite = pygame.transform.flip(sprite, flip_x, flip_y)

        pos = self.calculate_pos(x, y)

        screen.blit(sprite, pos)

        return pos

    
    def change_direction(self, direction):
        self.direction = direction
        if direction in [DIRECTION_LEFT, DIRECTION_RIGHT]:
            self.image_direction = direction