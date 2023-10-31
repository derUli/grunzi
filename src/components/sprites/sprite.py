import constants.graphics
import os
import pygame

class Sprite(object):
    def __init__(self, sprite_dir, sprite = None):
        self.sprite = None
        self.walkable = True
        self.id = None

        if not sprite:
            return

        file = os.path.join(sprite_dir, sprite)
        image = pygame.image.load(file).convert_alpha()
    
        
        self.sprite = pygame.transform.scale(image, constants.graphics.SPRITE_SIZE)
        
    def draw(self, screen, x, y):
        if not self.sprite:
            return

        width = self.sprite.get_width()
        height = self.sprite.get_height()
        pos = (width * x, height * y)

        screen.blit(self.sprite, pos)
