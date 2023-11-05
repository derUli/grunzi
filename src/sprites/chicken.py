""" Main character sprite """

import pygame
import random
import time
import logging
import os
from sprites.character import Character
from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT
from utils.audio import play_sound
class Chicken(Character):
    """ Chicken sprite class """

    def __init__(self, sprite_dir, cache, sprite='chicken.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction
        self.sound = None
        self.next_direction_change = time.time()

    def draw(self, screen, x, y):
        """ Draw sprite """

        if time.time() > self.next_direction_change:
            self.calculate_next_direction_change()

        sprite = self.sprite.copy()

        flip_x = False
        flip_y = False

        if self.image_direction == DIRECTION_LEFT:
            flip_x = True
        sprite = pygame.transform.flip(sprite, flip_x, flip_y)

        pos = self.calculate_pos(x, y)

        screen.blit(sprite, pos)

        return pos

    def calculate_next_direction_change(self):
        if self.direction == DIRECTION_LEFT:
            self.change_direction(DIRECTION_RIGHT)
            self.play_sound()
        else:
            self.change_direction(DIRECTION_LEFT)
            self.play_sound()

        self.next_direction_change = time.time() + random.randint(1, 6)

        return self.next_direction_change

    def play_sound(self):
        if self.sound and self.sound.get_busy():
            logging.debug('busy')
            return

        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'chicken')
        )

        # CREDITS: https://soundbible.com/1853-Raccoon.html
        files = [
            'chicken1.ogg',
            'chicken2.ogg',
            'chicken3.ogg',
            'chicken4.ogg',
            'chicken5.ogg',
            'chicken6.ogg'

        ]
        file = os.path.join(sound_dir, random.choice(files))

        self.sound = play_sound(file)


    def change_direction(self, direction):
        """ Change sprite direction """
        self.direction = direction
        if direction in [DIRECTION_LEFT, DIRECTION_RIGHT]:
            self.image_direction = direction
