""" Main character sprite """

import logging
import os
import random
import time

import pygame

from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_DOWN
from sprites.chainsaw import Chainsaw
from sprites.character import Character
from sprites.killable import Killable
from sprites.maincharacter import PIG_SOUND_NOTHING
from sprites.weapon import Weapon
from utils.audio import play_sound, sounds_busy

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0

BLOOD_COLOR = (163, 8, 8)
KITTEN_SOUND_FADEOUT = 100


class Kitten(Killable, Character):
    """ Chicken sprite class """

    def __init__(self, sprite_dir, cache, sprite='kitten.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction
        self.sound = None
        # Time until next move
        self.walk_speed = 0.3

        self.next_mew = time.time() + random.randint(10, 30)

    def draw(self, screen, x, y):
        """ Draw sprite """
        self.play_sound()
        sprite = self.sprite.copy()

        flip_x = False
        flip_y = False

        if self.image_direction == DIRECTION_LEFT:
            flip_x = True

        sprite = pygame.transform.flip(sprite, flip_x, flip_y)

        pos = self.calculate_pos(x, y)

        screen.blit(sprite, pos)

    def random_direction(self):
        direction = random.choice([
            DIRECTION_LEFT,
            DIRECTION_RIGHT,
            DIRECTION_UP,
            DIRECTION_DOWN
        ])

        if direction == self.direction:
            return self.random_direction()

        return direction

    def play_sound(self):
        if sounds_busy():
            return

        if not self.next_mew:
            return
        if time.time() < self.next_mew:
            return

        self.next_mew = time.time() + random.randint(10, 30)

        sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'kitten')
        )

        # CREDITS: https://soundbible.com/1853-Raccoon.html
        files = [
            'kitten1.ogg',
            'kitten2.ogg',
            'kitten3.ogg',
            'kitten4.ogg',
            'kitten5.ogg',
            'kitten6.ogg'

        ]
        file = os.path.join(sound_dir, random.choice(files))

        self.sound = play_sound(file)

    def change_direction(self, direction):
        """ Change sprite direction """
        self.direction = direction
        if direction in [DIRECTION_LEFT, DIRECTION_RIGHT]:
            self.image_direction = direction

    def handle_interact(self, element):
        self.change_direction(self.random_direction())
        element.play_sound(PIG_SOUND_NOTHING)

    def handle_interact_item(self, element):
        """ Handle interact """
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

            self.walkable = True

            if self.sound and self.sound.get_busy():
                self.sound.fadeout(KITTEN_SOUND_FADEOUT)

            logging.debug('Kitten killed by chainsaw')

            self.start_fade()

            element.state.inventory.play_sound()

            # Rumble on gamepad if we have one
            if element.state.gamepad:
                element.state.gamepad.joystick.rumble(
                    RUMBLE_CHAINSAW_LOW_FREQUENCY,
                    RUMBLE_CHAINSAW_HIGH_FREQUENCY,
                    RUMBLE_CHAINSAW_DURATION
                )

        elif isinstance(element.state.inventory, Weapon):
            self.kill()

    def ai(self, level):
        if time.time() < self.last_movement + self.walk_speed:
            return

        z, y, x = level.search_sprite(self)

        next_x = x
        next_y = y

        if self.direction == DIRECTION_LEFT:
            next_x -= 1
        elif self.direction == DIRECTION_RIGHT:
            next_x += 1
        elif self.direction == DIRECTION_UP:
            next_y -= 1
        elif self.direction == DIRECTION_DOWN:
            next_y += 1

        walkable = level.is_walkable(next_x, next_y)

        if walkable:
            level.move_sprite(self, (z, next_y, next_x))
            self.last_movement = time.time()
