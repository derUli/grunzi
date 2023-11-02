from constants.headup import UI_MARGIN
import pygame
import os
import utils.audio
import random


class PlayerState():

    def __init__(self, data_dir):
        self.health = 100
        self.show_detailed = None
        self.inventory = None

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
        self.health = 100
        self.update_health()

    def partial_heal(self, health):
        self.health += health
        self.update_health()

    def hurt(self, health):
        self.health -= health
        self.update_health()
        sound = random.choice(self.hurt_sounds)

        utils.audio.play_sound(sound)

    def dead(self):
        return self.health <= 0

    def update_health(self):
        if self.health < 1:
            self.health = 0

        if self.health > 99:
            self.health = 100

        self.crop_pig()

    def crop_pig(self):
        width = self.health_pig.get_width()
        height = self.health_pig.get_width()
        one_percent = height / 100
        new_height = one_percent * self.health

        self.cropped_pig = pygame.Surface((width, new_height), pygame.SRCALPHA)
        self.cropped_pig.blit(self.health_pig, (0, 0))

    def draw_ui(self, screen):
        self.draw_health(screen)
        self.draw_inventory(screen)

    def draw_health(self, screen):
        str(self.health).ljust(3, ' ')
        pig_width = self.cropped_pig.get_width()

        pos = (
            screen.get_width() - pig_width -
            UI_MARGIN,
            UI_MARGIN,
        )

        screen.blit(self.cropped_pig, pos)

    def draw_inventory(self, screen):
        size = self.inventory_image.get_size()

        surface = pygame.surface.Surface(size)

        surface.set_alpha(0)

        surface.blit(self.inventory_image, (0,0))

        x, y = screen.get_size()

        x = x - surface.get_width() - UI_MARGIN
        y = y - surface.get_height() - UI_MARGIN

        screen.blit(surface, (x, y))
        