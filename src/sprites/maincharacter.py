""" Main character sprite """
import os
import pygame
import constants.game
from sprites.character import Character
from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_UP
from utils.audio import play_sound
from sprites.inlinesprite import InlineSprite
from components.fadeable_component import FadeableComponent
PIG_SOUND_NOTHING = 'nothing.ogg'


class MainCharacter(Character, FadeableComponent):
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

    def draw(self, screen, x, y):
        """ Draw main character """
        super().draw(screen, x, y)

        self.draw_inventory_item(screen, x, y)

        # Detailed object view
        if self.state.show_detailed:
            screen.blit(self.state.show_detailed, (0, 0))


    def draw_inventory_item(self, screen, x, y):
        """ Draw inventory item """
        if not isinstance(self.state.inventory, InlineSprite):
            return

        if not self.state.use_item:
            return

        sprite = self.state.inventory.sprite.copy().convert_alpha()

        if self.direction == DIRECTION_UP:
            sprite = pygame.transform.rotate(sprite, 90)
            y -= 1
        elif self.direction == DIRECTION_DOWN:
            sprite = pygame.transform.rotate(sprite, 270)
            y += 1
        elif self.direction == DIRECTION_RIGHT:
            x += 1
        elif self.direction == DIRECTION_LEFT:
            sprite = pygame.transform.flip(sprite, flip_x = True, flip_y= False)
            x -= 1

        pos = self.calculate_pos(x, y)
        screen.blit(sprite, pos)


    def play_sound(self, sound):
        if self.sound and self.sound.get_busy():
            return

        sound_dir = os.path.join(self.sound_dir, sound)
        self.sound = play_sound(sound_dir)
