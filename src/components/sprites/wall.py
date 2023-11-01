import constants.graphics
import os
import pygame
import components.sprites.sprite


class Wall(components.sprites.sprite.Sprite):

    def __init__(self, sprite_dir, cache, sprite=None):
        super().__init__(sprite_dir, cache, 'wall.jpg')
        self.walkable = False
