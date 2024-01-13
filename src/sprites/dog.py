""" Dog character sprite """

import logging
import os
import random
import time

import pygame

from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT
from constants.game import MAIN_CHARACTER_ID
from sprites.chainsaw import Chainsaw
from sprites.character import Character
from sprites.killable import Killable
from sprites.maincharacter import PIG_SOUND_NOTHING
from sprites.weapon import Weapon
from utils.audio import play_sound

BLOOD_COLOR = (163, 8, 8)
SOUND_FADEOUT = 100
HURT_DAMAGE = 5


class Dog(Killable, Character):
    """ Dog sprite class """

    def __init__(self, sprite_dir, cache, sprite='dog.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction
        self.sound = None
        self.next_direction_change = None
        # Time until next move
        self.walk_speed = 0.5

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

    def play_sound(self):
        if self.sound and self.sound.get_busy():
            return

        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'dog')
        )

        # CREDITS: https://soundbible.com/1853-Raccoon.html
        files = [
            'dog1.ogg',
            'dog2.ogg'

        ]
        file = os.path.join(sound_dir, random.choice(files))

        self.sound = play_sound(file)

    def handle_interact_item(self, element):
        """ Handle interact """
        logging.debug('interact')
        # Destroy if player has the chainsaw
        if not element:
            return

        if self.killed():
            return

        if self.walkable:
            return

        # Chicken is killed by chainsaw
        if isinstance(element.state.inventory, Chainsaw):
            if element.state.inventory.attributes['fuel'] <= 0:
                return

            self.kill()

            if self.sound and self.sound.get_busy():
                self.sound.fadeout(SOUND_FADEOUT)

            logging.debug('Dog killed by chainsaw')

            element.state.inventory.play_sound()

            self.rumble(element.state.gamepad)
        elif isinstance(element.state.inventory, Weapon):
            self.kill()
        else:
            element.play_sound(PIG_SOUND_NOTHING)

    def ai(self, level):
        print()
        if time.time() - self.last_movement < self.walk_speed:
            return

        self.last_movement = time.time()

        mainchar_z, mainchar_y, mainchar_x = level.search_by_id(
            MAIN_CHARACTER_ID)
        dog_z, dog_y, dog_x = level.search_sprite(self)

        new_y = dog_y
        new_x = dog_x

        if mainchar_y > new_y:
            new_y += 1
        if mainchar_x > new_x:
            new_x += 1
            self.change_direction(DIRECTION_RIGHT)
        if mainchar_y < new_y:
            new_y -= 1
        if mainchar_x < new_x:
            new_x -= 1
            self.change_direction(DIRECTION_LEFT)

        move_options = [
            (new_x, dog_y),
            (dog_x, new_y)
        ]

        # Attacks piggy
        if new_y == mainchar_y and new_x == mainchar_x:
            mainchar = level.layers[mainchar_z][mainchar_y][mainchar_x]
            self.play_sound()
            mainchar.state.hurt(HURT_DAMAGE)

        for option in move_options:
            target_x, target_y = option
            if level.is_walkable(target_x, target_y):
                level.layers[dog_z][target_y][target_x] = self
                level.layers[dog_z][dog_y][dog_x] = None
                break

    def handle_interact(self, element):
        return
