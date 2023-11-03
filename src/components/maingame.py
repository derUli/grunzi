import math
import os
import time

import pygame

import constants.game
import constants.graphics
import state.state
import utils.savegame
from components.component import Component
from components.gameover import GameOver
from components.pausable_component import PausableComponent
from constants.direction import *
from constants.headup import BOTTOM_UI_HEIGHT
from state.level import Level

MOVEMENT_KEYS = [
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_UP,
    pygame.K_DOWN
]

CONFIRM_KEYS = [
    pygame.K_SPACE,
    pygame.K_RETURN,
]

DISCARD_KEYS = MOVEMENT_KEYS + CONFIRM_KEYS


class MainGame(PausableComponent, Component):

    def __init__(self, data_dir, handle_change_component, settings_state):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state)

        self.state = state.state.State(self.data_dir)
        self.sprites_dir = os.path.join(self.data_dir, 'images', 'sprites')
        self.level = Level(self.sprites_dir, self.image_cache)
        self.camera_offset = [0, 0]
        self.moving = None
        self.running = False

        background_file = os.path.join(
            self.sprites_dir, 'backdrops', 'landscape.jpg'
        )

        self.backdrop = pygame.image.load(background_file).convert_alpha()
        self.backdrop = pygame.transform.smoothscale(
            self.backdrop, constants.game.SCREEN_SIZE)

    def load_savegame(self):
        """ Load savegame """
        level_file = utils.savegame.load_game(utils.savegame.DEFAULT_SAVE, self.state)
        self.load_level(level_file)

    def load_level(self, level_file):
        self.level.level_file = level_file
        self.level.load()

        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)
        self.level.layers[z][y][x].state = self.state.player_state

        self.update_camera()

    def mount(self):
        pygame.mouse.set_visible(0)

        atmo = 'level' + str(self.state.level) + '.ogg'
        self.play_music(atmo)

        level_file = os.path.join(self.data_dir, 'levels', 'level1.json')
        self.load_level(level_file)

    def unmount(self):
        pygame.mouse.set_visible(1)
        pygame.mixer.music.stop()

    def update_screen(self, screen):

        if self.moving:
            self.move_main_character(self.moving)

        self.level.purge_sprites()
        sprite_width, sprite_height = constants.graphics.SPRITE_SIZE

        w, h = screen.get_size()

        h -= BOTTOM_UI_HEIGHT
        virtual_screen = pygame.surface.Surface((w, h))

        virtual_screen.blit(self.backdrop, (0, 0))

        tolerance_x = math.ceil(w / sprite_width)
        tolerance_y = math.ceil(h / sprite_height)

        filtered_layers = list(self.level.layers)

        for z in range(0, len(filtered_layers)):
            from_y = self.camera_offset[1] - math.ceil(tolerance_y / 2)
            to_y = self.camera_offset[1] + tolerance_y

            from_x = self.camera_offset[0] - math.ceil(tolerance_x / 2)
            to_x = self.camera_offset[0] + tolerance_x

            if from_y < 0:
                from_y = 0

            if from_x < 0:
                from_x = 0

            filtered_layers[z] = filtered_layers[z][from_y:to_y]

            for y in range(0, len(filtered_layers[z])):
                filtered_layers[z][y] = filtered_layers[z][y][from_x:to_x]

        for layer in filtered_layers:
            y = 0
            x = 0
            for row in layer:
                for col in row:
                    if col:
                        col.draw(virtual_screen, x, y)
                    x += 1

                y += 1
                x = 0

        self.screen.blit(virtual_screen, (0, 0))

        self.draw_headup(self.screen)

        if self.state.player_state.dead():
            component = self.handle_change_component(GameOver)
            component.state = self.state

    def update_camera(self):
        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)

        if x < 0:
            x = 0

        if y < 0:
            y = 0

        self.camera_offset = [x, y]

    def handle_event(self, event):
        """ Handle events """
        super().handle_event(event)

        if event.type == pygame.KEYUP:
            self.handle_keyup_event(event)
        elif event.type == pygame.KEYDOWN:
            self.handle_keydown_event(event)

    def handle_keydown_event(self, event):
        """" Handle keydown events """
        if event.key in DISCARD_KEYS and self.state.player_state.show_detailed:
            self.state.player_state.show_detailed = None
        elif event.key == pygame.K_LEFT:
            self.move_main_character(DIRECTION_LEFT)
        elif event.key == pygame.K_RIGHT:
            self.move_main_character(DIRECTION_RIGHT)
        elif event.key == pygame.K_UP:
            self.move_main_character(DIRECTION_UP)
        elif event.key == pygame.K_DOWN:
            self.move_main_character(DIRECTION_DOWN)
        elif event.key == pygame.K_LSHIFT:
            self.running = True

    def handle_keyup_event(self, event):
        """" Handle keyup events """
        if event.key in MOVEMENT_KEYS:
            self.moving = None
        elif event.key == pygame.K_LSHIFT:
            self.running = False

    def move_main_character(self, direction):
        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)
        character = self.level.layers[z][y][x]

        if not self.moving:
            self.moving = direction
            character.last_move = 0
            return

        walk_speed = character.walk_speed

        if self.running:
            walk_speed = character.sprint_speed

        if time.time() - character.last_move < walk_speed:
            return

        character.last_move = time.time()

        next_x = x
        next_y = y

        if direction == DIRECTION_UP:
            next_y -= 1
        elif direction == DIRECTION_LEFT:
            next_x -= 1
        elif direction == DIRECTION_RIGHT:
            next_x += 1
        elif direction == DIRECTION_DOWN:
            next_y += 1

        character.change_direction(direction)

        if (next_y < 0):
            return

        if (next_x < 0):
            return

        if (next_y > len(self.level.layers[z]) - 1):
            return

        if (next_x > len(self.level.layers[z][y]) - 1):
            return

        walkable = True
        layer_count = len(self.level.layers)

        for layer in range(0, layer_count):
            element = self.level.layers[layer][next_y][next_x]
            if element:
                element.handle_interact(character)

                if not element.walkable:
                    walkable = False

        if walkable:
            self.level.layers[z] = self.level.fill_fallback(None)
            self.level.layers[z][next_y][next_x] = character

            self.update_camera()

    def draw_headup(self, screen):
        """ Draw head up display """
        self.state.player_state.draw(screen)
