import constants.graphics
import os
import pygame

class Sprite(object):
    def __init__(self, sprite_dir, sprite = None):
        file = os.path.join(sprite_dir, sprite)
        image = pygame.image.load(file).convert_alpha()
        self.sprite = pygame.transform.scale(image, constants.graphics.SPRITE_SIZE)
        
    def draw(self, screen, x, y):
        width = self.sprite.get_width()
        height = self.sprite.get_height()
        pos = (width * x, height * y)

        screen.blit(self.sprite, pos)
