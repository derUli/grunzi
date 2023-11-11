import gettext
import logging
import os
import random
import time

import pygame

import utils.quality
from constants.headup import UI_MARGIN, BOTTOM_UI_HEIGHT, BOTTOM_UI_BACKGROUND
from sprites.inlinesprite import InlineSprite
from utils.audio import play_sound
from utils.display_text import DisplayText

_ = gettext.gettext

FULL_HEALTH = 100
INVENTORY_PADDING = 10
FLASH_COLOR_HURT = (255, 0, 0,)
FLASH_COLOR_HEAL = (255, 255, 255)
RUMBLE_DURATION_PAIN = 200
RUMBLE_LOW_FREQUENCY = 1
RUMBLE_HIGH_FREQUENCY = 1


class PlayerState:
    def __init__(self, data_dir, gamepad=None):
        """ Constructor """
        self.health = FULL_HEALTH
        self.show_detailed = None
        self.inventory = None
        self.flashing = None
        self.flash_start = 0
        self.flash_duration = 0.05
        self.gamepad = gamepad
        self.use_item = False
        self.display_text = DisplayText(data_dir)
        self.data_dir = data_dir

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

    def flash(self, color=FLASH_COLOR_HURT):
        """ Flashing effect in color """
        self.flashing = color
        self.flash_start = time.time()

    def hurt(self, health):
        """ Hurt piggy """
        self.health -= health
        sound = random.choice(self.hurt_sounds)
        play_sound(sound)
        self.flash(FLASH_COLOR_HURT)
        self.update_health()
        self.say(_('Autsch!'))

        if self.gamepad:
            self.gamepad.joystick.rumble(RUMBLE_LOW_FREQUENCY, RUMBLE_HIGH_FREQUENCY, RUMBLE_DURATION_PAIN)

    def say(self, text):
        self.display_text.show_text(text)

    def toggle_item(self):
        """ Toggle use item """
        if not self.inventory:
            self.use_item = False
            return

        if not isinstance(self.inventory, InlineSprite):
            sound = os.path.abspath(
                os.path.join(
                    self.data_dir,
                    'sounds',
                    'common',
                    'beep.ogg'
                )
            )

            play_sound(sound)
            return

        self.use_item = not self.use_item

    def dead(self):
        if self.health > 0:
            return False

        return True

    def update_health(self):
        """ Normalize health and update pig image """

        if self.health < 0:
            self.health = 0
        if self.health > 99:
            self.health = 100

        logging.debug('Current health: ' + str(self.health))
        self.crop_pig()

    def crop_pig(self):
        """ Crop the pig image based on current health """
        width = self.health_pig.get_width()
        height = self.health_pig.get_width()
        one_percent = height / 100
        new_height = one_percent * self.health

        if new_height < 1:
            self.cropped_pig = pygame.surface.Surface((1, 1), pygame.SRCALPHA)
            return

        self.cropped_pig = pygame.surface.Surface(
            (width, new_height), pygame.SRCALPHA)
        self.cropped_pig.blit(self.health_pig, (0, 0))

    def draw(self, screen):
        """ Draw player state UI """
        self.draw_flash(screen)
        self.draw_background(screen)
        self.draw_health(screen)
        self.draw_inventory(screen)
        self.draw_text(screen)

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
        self.use_item = False

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

        surface = pygame.surface.Surface(size, pygame.SRCALPHA)
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

            scaled_item_sprite = utils.quality.scale_method()(
                self.inventory.sprite,
                (target_w, target_h)
            )

            surface.blit(scaled_item_sprite, (INVENTORY_PADDING, INVENTORY_PADDING))

        screen.blit(surface, (x, y))

    def draw_text(self, screen):
        """ Draw ui background """

        if not self.display_text.rendered_text:
            return

        w, h = self.display_text.rendered_text.get_size()

        x = (screen.get_width() / 2) - (w / 2)
        y = screen.get_height() - (BOTTOM_UI_HEIGHT / 2) - (h / 2) - UI_MARGIN

        self.display_text.draw(screen, (x, y))
