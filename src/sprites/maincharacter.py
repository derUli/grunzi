""" Main character sprite """
import os

import pygame

import constants.game
from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_UP
from sprites.character import Character
from sprites.inlinesprite import InlineSprite
from utils.audio import play_sound

PIG_SOUND_NOTHING = 'nothing.ogg'


class MainCharacter(Character):
    """ Main character sprite class """

    def __init__(self, sprite_dir, cache, sprite='pig.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.center_camera = True
        self.sound = None

        self.last_movement = 0
        self.id = constants.game.MAIN_CHARACTER_ID
        self.sound_dir = os.path.abspath(
            os.path.join(self.sprite_dir, '..', '..', 'sounds', 'pig')
        )

        self.walk_speed = 0.085
        self.sprint_speed = self.walk_speed * 0.7

    def draw(self, screen, x, y):
        """ Draw main character """
        drawn = super().draw(screen, x, y)

        self.draw_inventory_item(screen, x, y)

        # Detailed object view
        if self.state and self.state.show_detailed:
            screen.blit(self.state.show_detailed, (0, 0))

        return drawn

    def draw_inventory_item(self, screen, x, y):
        if not self.state:
            return
        """ Draw inventory item """
        if not isinstance(self.state.inventory, InlineSprite):
            return

        if not self.state.use_item:
            return

        item = self.state.inventory
        sprite = item.sprite.copy().convert_alpha()

        if self.direction == DIRECTION_UP:
            sprite = pygame.transform.rotate(sprite, 90)
            y -= 1
        elif self.direction == DIRECTION_DOWN:
            sprite = pygame.transform.rotate(sprite, 270)
            y += 1
        elif self.direction == DIRECTION_RIGHT:
            x += 1
        elif self.direction == DIRECTION_LEFT:
            sprite = pygame.transform.flip(sprite, flip_x=True, flip_y=False)
            x -= 1

        item.inline_sprite = sprite.convert_alpha()
        item.draw_inline(
            screen,
            self.calculate_pos(x, y)
        )

    def play_sound(self, sound):
        """ Play a sound """
        if self.sound and self.sound.get_busy():
            return

        sound_dir = os.path.join(self.sound_dir, sound)
        self.sound = play_sound(sound_dir)
