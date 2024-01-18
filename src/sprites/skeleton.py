""" Main character sprite """

import logging
import time

import pygame

from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT
from constants.graphics import SPRITE_SIZE
from constants.headup import NPC_HEALTH_COLOR_ENEMY, NPC_HEALTH_HEIGHT
from sprites.chainsaw import Chainsaw
from sprites.character import Character
from sprites.killable import Killable
from sprites.sword import Sword

BLOOD_COLOR = (163, 8, 8)
CHICKEN_SOUND_FADEOUT = 100
CHAINSAW_DAMAGE = 2
SWORD_DAMAGE = 5
HURT_DAMAGE = 10


class Skeleton(Killable, Character):
    """ Skeleton sprite class """

    def __init__(self, sprite_dir, cache, sprite='skeleton.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)
        self.sentence = -1
        self.attributes = {
            'health': 100
        }

        self.walk_speed = 0.8

    def draw(self, screen, x, y):
        super().draw(screen, x, y)

        pos = self.calculate_pos(x, y)

        self.draw_health(screen, pos)

    def draw_health(self, screen, pos):

        x, y = pos
        w, h = SPRITE_SIZE

        y += h - NPC_HEALTH_HEIGHT

        w = w / 100 * self.attributes['health']
        h = NPC_HEALTH_HEIGHT

        if w < 1:
            return

        surface = pygame.surface.Surface((w, h))

        surface.fill(NPC_HEALTH_COLOR_ENEMY)

        screen.blit(surface, (x, y))

    def handle_interact_item(self, element):
        """ Handle interact """
        logging.debug('interact')
        # Destroy if player has the chainsaw
        if not element:
            return

        if self.purge:
            return

        # Chicken is killed by chainsaw
        if isinstance(element.state.inventory, Chainsaw):
            if element.state.inventory.attributes['fuel'] <= 0:
                return

            self.rumble(element.state.gamepad)

            self.attributes['health'] -= CHAINSAW_DAMAGE

            element.state.inventory.play_sound()

        elif isinstance(element.state.inventory, Sword):
            self.attributes['health'] -= SWORD_DAMAGE

        if self.attributes['health'] <= 0:
            self.attributes['health'] = 0

            logging.debug('Skeleton killed')
            self.kill()

    def ai(self, level):
        if time.time() - self.last_movement < self.walk_speed:
            return

        self.last_movement = time.time()

        mainchar_z, mainchar_y, mainchar_x = level.search_mainchar()
        me_z, me_y, me_x = level.search_sprite(self)

        new_y = me_y
        new_x = me_x

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
            (new_x, me_y),
            (me_x, new_y)
        ]

        # Attacks piggy
        if new_y == mainchar_y and new_x == mainchar_x:
            mainchar = level.layers[mainchar_z][mainchar_y][mainchar_x]
            # self.play_sound()
            mainchar.state.hurt(HURT_DAMAGE)

        for option in move_options:
            target_x, target_y = option
            if level.is_walkable(target_x, target_y):
                level.layers[me_z][target_y][target_x] = self
                level.layers[me_z][me_y][me_x] = None
                break
