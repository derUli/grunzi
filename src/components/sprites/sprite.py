import constants.graphics
import os
import pygame

class Sprite(object):
    def __init__(self, sprite_dir, cache, sprite = None):
        self.sprite = None
        self.walkable = True
        self.sprite_dir = sprite_dir
        self.id = None

        self.center_camera = False

        if not sprite:
            return

        file = os.path.join(sprite_dir, sprite)
        image = cache.load_image(file)
    
        
        self.sprite = pygame.transform.scale(image, constants.graphics.SPRITE_SIZE)
        
    def draw(self, screen, x, y):
        if not self.sprite:
            return

        pos = self.calculate_pos(x, y)

        screen.blit(self.sprite, pos)

        return pos


    def calculate_pos(self, x, y):
        if not self.sprite:
            return

        width = self.sprite.get_width()
        height = self.sprite.get_height()
        return (width * x, height * y)

    def handle_interact(self, object):
        return

    def change_direction(self, direction):
        return 