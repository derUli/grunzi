""" Main character sprite """

import logging
import os
import random
import time

import pygame

from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_DOWN
from sprites.chainsaw import Chainsaw
from sprites.character import Character
from sprites.feather import Feather
from sprites.killable import Killable
from sprites.maincharacter import PIG_SOUND_NOTHING
from sprites.weapon import Weapon
from utils.audio import play_sound, sounds_busy
from utils.quality import pixel_fades_enabled

RUMBLE_CHAINSAW_DURATION = 300
RUMBLE_CHAINSAW_HIGH_FREQUENCY = 1
RUMBLE_CHAINSAW_LOW_FREQUENCY = 0

BLOOD_COLOR = (163, 8, 8)
CHICKEN_SOUND_FADEOUT = 100


class Chicken(Killable, Character):
    """ Chicken sprite class """

    def __init__(self, sprite_dir, cache, sprite='chicken.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.walkable = False
        self.direction = DIRECTION_RIGHT
        self.image_direction = self.direction
        self.sound = None
        self.next_direction_change = time.time()
        # Time until next move
        self.walk_speed = random.randint(1, 3)

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

    def calculate_next_direction_change(self):
        self.change_direction(self.random_direction())
        self.play_sound()

        self.next_direction_change = time.time() + random.randint(1, 10)

        return self.next_direction_change

    def play_sound(self):
        if sounds_busy():
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
        if isinstance(element.state.inventory, Chainsaw) and not self.walkable:
            if element.state.inventory.attributes['fuel'] <= 0:
                return

            if self.sound and self.sound.get_busy():
                self.sound.fadeout(CHICKEN_SOUND_FADEOUT)

            self.start_fade()

            if not pixel_fades_enabled():
                self.stop_fade()

            logging.debug('Chicken killed by chainsaw')

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
        else:
            element.play_sound(PIG_SOUND_NOTHING)

    def ai(self, level):
        if time.time() < self.last_movement + self.walk_speed:
            return

        if time.time() > self.next_direction_change:
            self.calculate_next_direction_change()

        self.walk_speed = random.randint(1, 3)

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
        else:
            self.change_direction(self.random_direction())

    def stop_fade(self):
        self.fadeout = False
        # Replace chicken with feather
        self.replace_with = Feather(self.sprite_dir, self.cache)
