""" Racoon character """
import os

import constants.graphics
import constants.direction
import sprites.character
import utils.audio
import pygame

class Fire(sprites.character.Character):
    """ Fire character class """

    def __init__(self, sprite_dir, cache, sprite=None):
        """ Constructor """
    
        super().__init__(sprite_dir, cache, 'raccoon.png')
        sprite_dir = os.path.join(sprite_dir, 'animations', 'fire')

        self.walkable = False

        self.cache = cache
        self.frames = []

        files = os.listdir(sprite_dir)
        files.sort()
        
        for file in files:
            if file.endswith('.gif'):
                fullpath = os.path.join(sprite_dir, file)
                image = self.cache.load_image(fullpath)
                image.set_colorkey((11, 0, 0, 1))
                image = pygame.transform.scale(image, constants.graphics.SPRITE_SIZE)
                self.frames.append(image)

        self.current_frame = 0



   
    def draw(self, screen, x, y):
        print(self.current_frame)
        current_frame = self.frames[self.current_frame]
        pos = self.calculate_pos(x, y)
        
        screen.blit(current_frame, pos)
        self.next_frame()

    
    def next_frame(self):
        next_frame = self.current_frame + 1

        if next_frame >= len(self.frames):
            next_frame = 0

        self.current_frame = next_frame