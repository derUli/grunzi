import logging
import os
import random
import time

import numpy
import pygame
from PygameShader.shader import blood
import utils.quality
from constants.headup import UI_MARGIN, BOTTOM_UI_HEIGHT, BOTTOM_UI_BACKGROUND
from sprites.inlinesprite import InlineSprite
from utils.audio import play_sound
from utils.display_text import DisplayText

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
        self.rendered_ui = (None, None)
        self.use_item = False
        self.display_text = DisplayText(data_dir)
        self.data_dir = data_dir
        self.drawn_inventory = None
        self.drawn_health = None
        self.health_pig = pygame.image.load(
            os.path.join(data_dir, 'images', 'ui',
                         'health.png')
        ).convert_alpha()

        self.blood_surface = pygame.image.load(
            os.path.join(data_dir, 'images', 'ui',
                         'blood.png')
        ).convert_alpha()

        self.blood_mask = None

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
        self.update_health()
        self.say(_('Ouch!'))

        if self.gamepad:
            self.gamepad.joystick.rumble(
                RUMBLE_LOW_FREQUENCY,
                RUMBLE_HIGH_FREQUENCY,
                RUMBLE_DURATION_PAIN)

    def say(self, text):
        """ Display text in bottom UI """
        self.display_text.show_text(text)

    def toggle_item(self):
        """ Toggle use item """
        if not self.inventory:
            self.use_item = False
            return

        if not self.inventory.player_state:
            self.inventory.player_state = self

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
        """ Check if player is dead """
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

    def to_dict(self):
        """ Player state to dict """
        data = {
            'health': self.health,
            'use_item': self.use_item,
        }

        if self.inventory and self.inventory.sprite:
            data['inventory'] = hash(
                pygame.image.tostring(
                    self.inventory.sprite,
                    'RGB'
                )
            )

        if self.display_text.rendered_text:
            data['rendered_text'] = hash(
                pygame.image.tostring(
                    self.display_text.rendered_text,
                    'RGB'
                )
            )

        return data

    def to_hash(self):
        """ Hashsum from player state values """
        return hash(str(self.to_dict()))

    def draw(self, screen):
        """ Draw player state UI """
        self.draw_blood(screen)
        self.draw_flash(screen)

        id_string, surf = self.rendered_ui
        y = screen.get_height() - BOTTOM_UI_HEIGHT

        if self.to_hash() == id_string:
            drawn = screen.blit(surf, (0, y))
            self.draw_text(screen)
            return drawn

        size = (screen.get_width(), BOTTOM_UI_HEIGHT)
        surf = pygame.surface.Surface(size, pygame.SRCALPHA)

        self.draw_background(surf)
        self.draw_health(surf)
        self.draw_inventory(surf)

        id_string = self.to_hash()
        self.rendered_ui = (id_string, surf)
        drawn = screen.blit(surf, (0, y))
        self.draw_text(screen)

        return drawn

    def draw_blood(self, screen):
        if not utils.quality.blood_enabled():
            return

        """ Draw bloody screen overlay """
        if self.health == 100:
            return
        if self.blood_surface.get_size() != screen.get_size():
            self.blood_surface = utils.quality.scale_method()(
                self.blood_surface,
                screen.get_size()
            )

            self.blood_mask = numpy.asarray(
                pygame.surfarray.pixels_alpha(
                    self.blood_surface) / 255.0, numpy.float32
            )

        if self.blood_mask is None:
            self.blood_mask = numpy.asarray(
                pygame.surfarray.pixels_alpha(
                    self.blood_surface) / 255.0, numpy.float32
            )

        percentage = 1.0 - (self.health / 100)

        if (percentage <= 0):
            return

        # Low quality blood
        if not utils.quality.blood_enabled_high():
            self.blood_surface.set_alpha(255 / 100 * (percentage * 100))
            screen.blit(self.blood_surface, (0, 0))
            return

        blood(screen, self.blood_mask, percentage)

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

        if not item.walkable:
            return

        self.inventory = item
        self.use_item = False

        return True

    def draw_health(self, screen):
        """ Draw health display """
        surface = self.health_pig

        x, y = screen.get_size()
        x = x - surface.get_width() - UI_MARGIN
        y = UI_MARGIN

        self.drawn_health = screen.blit(self.cropped_pig, (x, y))

    def draw_background(self, screen):
        """ Draw ui background """

        screen.fill(BOTTOM_UI_BACKGROUND)

    def draw_inventory(self, screen):
        """ Draw inventory """
        size = self.inventory_image.get_size()

        surface = pygame.surface.Surface(size, pygame.SRCALPHA)
        surface.blit(self.inventory_image, (0, 0))

        x = UI_MARGIN
        y = UI_MARGIN

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

            surface.blit(
                scaled_item_sprite,
                (INVENTORY_PADDING,
                 INVENTORY_PADDING))

        self.drawn_inventory = screen.blit(surface, (x, y))

    def draw_text(self, screen):
        """ Draw ui background """

        if not self.display_text.rendered_text:
            return

        w, h = self.display_text.rendered_text.get_size()

        x = (screen.get_width() / 2) - (w / 2)
        y = screen.get_height() - (BOTTOM_UI_HEIGHT / 2) - (h / 2) - UI_MARGIN

        self.display_text.draw(screen, (x, y))
