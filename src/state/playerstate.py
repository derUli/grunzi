import logging
import os
import random
import time

import pygame

from constants.headup import UI_MARGIN, BOTTOM_UI_HEIGHT, BOTTOM_UI_BACKGROUND
from utils.audio import play_sound

FULL_HEALTH = 100
INVENTORY_PADDING = 10
FLASH_COLOR_HURT = (255, 0, 0,)
FLASH_COLOR_HEAL = (255, 255, 255)


class PlayerState:
    def __init__(self, data_dir):
        """ Constructor """
        self.health = FULL_HEALTH
        self.show_detailed = None
        self.inventory = None
        self.flashing = None
        self.flash_start = 0
        self.flash_duration = 0.05

        self.health_pig = pygame.image.load(
            os.path.join(data_dir, 'images', 'ui',
                         'health.png')
        ).convert_alpha()

        self.inventory_image = pygame.image.load(
            os.path.join(data_dir, 'images', 'ui',
                         'inventory.png')

        ).convert_alpha()

        self.cropped_pig = None

        pig_sounds_dir = os.path.join(data_dir, 'sounds', 'pig')
        self.hurt_sounds = []

        for i in range(1, 5):
            self.hurt_sounds.append(
                os.path.join(pig_sounds_dir, 'pain' + str(i) + '.ogg'))

        self.update_health()

    def heal(self):
        """ Full heal the piggy """
        self.health = FULL_HEALTH
        self.update_health()
        self.flash(FLASH_COLOR_HEAL)

    def partial_heal(self, health):
        """ Partial heal the piggy """
        self.health += health
        self.update_health()
        self.flash(FLASH_COLOR_HEAL)

    def flash(self, color=(255, 0, 0,)):
        """ Flashing effect in color """
        self.flashing = color
        self.flash_start = time.time()

    def hurt(self, health):
        """ Hurt piggy """
        self.health -= health
        self.update_health()
        sound = random.choice(self.hurt_sounds)

        play_sound(sound)

        self.flash(FLASH_COLOR_HURT)

    def dead(self):
        """ Check if piggy is dead """
        return self.health <= 0

    def update_health(self):
        """ Normalize health and update pig image """
        if self.health < 1:
            self.health = 0

        if self.health > 99:
            self.health = 100

        logging.debug('Current health: ' + str(self.health))
        self.crop_pig()

    def crop_pig(self):
        """ Crop the pig image based on current health"""
        width = self.health_pig.get_width()
        height = self.health_pig.get_width()
        one_percent = height / 100
        new_height = one_percent * self.health

        self.cropped_pig = pygame.surface.Surface(
            (width, new_height), pygame.SRCALPHA)
        self.cropped_pig.blit(self.health_pig, (0, 0))

    def draw(self, screen):
        """ Draw player state UI """
        self.draw_flash(screen)
        self.draw_background(screen)
        self.draw_health(screen)
        self.draw_inventory(screen)

    def draw_flash(self, screen):
        """ Draw flash effect """
        if self.flashing:
            screen.fill(self.flashing)

        if time.time() - self.flash_start > self.flash_duration:
            self.flashing = None

    def take_item(self, item):
        """ Put item into inventory """
        if self.inventory:
            return False

        self.inventory = item

        return True

    def draw_health(self, screen):
        """ Draw health display """
        surface = self.health_pig

        x, y = screen.get_size()
        x = x - surface.get_width() - UI_MARGIN
        y = y - surface.get_height() - UI_MARGIN

        screen.blit(self.cropped_pig, (x, y))

    def draw_background(self, screen):
        """ Draw ui background """
        w = screen.get_width()
        h = BOTTOM_UI_HEIGHT

        x = 0
        y = screen.get_height() - h
        surface = pygame.surface.Surface((w, h))

        surface.fill(BOTTOM_UI_BACKGROUND)

        screen.blit(surface, (x, y))

    def draw_inventory(self, screen):
        """ Draw inventory """
        size = self.inventory_image.get_size()

        surface = pygame.surface.Surface(size)
        surface.blit(self.inventory_image, (0, 0))

        x, y = screen.get_size()
        x = UI_MARGIN
        y = y - surface.get_height() - UI_MARGIN

        # If inventory make item sprite fit into the frame
        if self.inventory and self.inventory.sprite:
            w, h = self.inventory.sprite.get_size()

            target_w = w - (INVENTORY_PADDING * 2)
            target_h = h - (INVENTORY_PADDING * 2)

            while target_w > surface.get_width() or target_h > surface.get_height():
                w -= 1
                h -= 1

            scaled_item_sprite = pygame.transform.smoothscale(
                self.inventory.sprite,
                (target_w, target_h)
            )

            surface.blit(scaled_item_sprite, (INVENTORY_PADDING, INVENTORY_PADDING))

        screen.blit(surface, (x, y))
