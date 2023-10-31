import constants.graphics
from constants.direction import *
import components.sprites.sprite
import pygame

class Character(components.sprites.sprite.Sprite):
    def __init__(self, sprite_dir, sprite = None):
        super().__init__(sprite_dir, 'pig.png')
        self.walkable = True
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction


    def draw(self, screen, x, y):

        sprite = self.sprite.copy()

        flip_x = False
        flip_y = False

        if(self.image_direction == DIRECTION_LEFT):
            flip_x = True

        sprite = pygame.transform.flip(sprite, flip_x, flip_y)

        width = sprite.get_width()
        height = sprite.get_height()

        pos = (width * x, height * y)

        screen.blit(sprite, pos)

    
    def change_direction(self, direction):
        self.direction = direction
        if direction in [DIRECTION_LEFT, DIRECTION_RIGHT]:
            self.image_direction = direction