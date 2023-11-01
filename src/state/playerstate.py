import constants.headup
import pygame
import os
import utils.audio
import random


class PlayerState():

    def __init__(self, data_dir):
        self.health = 100
        self.health_pig = pygame.image.load(
            os.path.join(data_dir, 'images', 'ui',
                         'health.png')).convert_alpha()
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

    def draw_health(self, screen):
        str(self.health).ljust(3, ' ')
        pig_width = self.cropped_pig.get_width()

        pos = [
            screen.get_width() - pig_width -
            constants.headup.HEALTH_PIG_POSITION[0],
            constants.headup.HEALTH_PIG_POSITION[1],
        ]

        screen.blit(self.cropped_pig, pos)
