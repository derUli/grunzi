import pygame
import os
import time
from constants.headup import BOTTOM_UI_HEIGHT
import constants.graphics
import constants.game
import state.state
import sprites.backdrop
import sprites.maincharacter
import sprites.fire
import sprites.wall
import sprites.raccoon
import sprites.detailed
from components.pausable_component import PausableComponent
from components.component import Component
from components.gameover import GameOver
from constants.direction import *
import utils.savegame
import random
import math

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

        super().__init__(data_dir, handle_change_component, settings_state)

        self.state = state.state.State(self.data_dir)
        self.sprites_dir = os.path.join(self.data_dir, 'images', 'sprites')
        self.layers = []
        self.camera_offset = [0, 0]
        self.moving = None
        self.running = False

        background_file = os.path.join(
            self.sprites_dir, 'backdrops', 'landscape.jpg')
        self.backdrop = pygame.image.load(background_file).convert_alpha()
        self.backdrop = pygame.transform.smoothscale(
            self.backdrop, constants.game.SCREEN_SIZE)

    def load_savegame(self):
        utils.savegame.load_game(utils.savegame.DEFAULT_SAVE, self.state)

    def fill_layers(self):
        # Three layers
        self.layers = [
            self.fill_fallback(
                sprites.backdrop.Backdrop),  # Backdrop layer
            self.fill_fallback(None),  # Static objects
            self.fill_fallback(None),  # Player character
        ]

        self.layers[0] = self.build_wall(self.layers[0])

        self.layers[1][0][5] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'dont_waste_water.png')

        self.layers[1][8][0] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'sunset.png')

        self.layers[1][3][4] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'bubblegum.png')

        main_character = sprites.maincharacter.MainCharacter(
            self.sprites_dir, self.image_cache)
        main_character.id = constants.game.MAIN_CHARACTER_ID
        main_character.state = self.state.player_state

        self.layers[2][5][3] = main_character

        self.camera_offset = (5, 3)
        self.update_camera()

        raccoon = sprites.raccoon.Raccoon(self.sprites_dir,
                                          self.image_cache)

        self.layers[1][7][8] = raccoon

        self.layers[1][0][10] = sprites.fire.Fire(
            self.sprites_dir,
            self.image_cache
        )

        self.layers[1][0][11] = sprites.fire.Fire(
            self.sprites_dir,
            self.image_cache
        )

        self.layers[1] = self.decorate_flowers(self.layers[1])

    def search_character(self, id):
        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if element and element.id == id:
                        return (z, y, x)

        return (0, 0, 0)

    def fill_fallback(self, callable):
        max_x, max_y = constants.game.LEVEL_1_SIZE

        rows = []

        for i in range(0, max_y):
            cols = []

            for n in range(0, max_x):
                s = None
                if callable:
                    s = callable(self.sprites_dir, self.image_cache)
                cols.append(s)

            rows.append(cols)

        return rows

    def build_wall(self, layer):

        for y in range(0, len(layer)):
            for x in range(0, len(layer[y])):
                is_wall = False
                if y == 0 or y == len(layer) - 1:
                    is_wall = True

                if x == 0 or x == len(layer[y]) - 1:
                    is_wall = True

                if is_wall:
                    layer[y][x] = sprites.wall.Wall(
                        self.sprites_dir, self.image_cache)

        return layer

    def decorate_flowers(self, layer):
        flowers = [
            'flower1.png',
            'flower2.png',
            'flower3.png',
            'flower4.png'
        ]
        for y in range(0, len(layer)):
            for x in range(0, len(layer[y])):

                layers_count = len(self.layers)

                walkable = True
                for z in range(0, layers_count):
                    if self.layers[z][y][x]:
                        if not self.layers[z][y][x].walkable:
                            walkable = False
                place_flower = random.randint(1, 10) == 2

                if walkable and place_flower:
                    layer[y][x] = sprites.backdrop.Backdrop(
                        self.sprites_dir, self.image_cache, random.choice(
                            flowers)
                    )

        return layer

    def mount(self):
        pygame.mouse.set_visible(0)

        atmo = 'level' + str(self.state.level) + '.ogg'
        self.play_music(atmo)
        self.fill_layers()

    def unmount(self):
        pygame.mouse.set_visible(1)
        pygame.mixer.music.stop()

    def update_screen(self, screen):

        if self.moving:
            self.move_main_character(self.moving)

        level_size_fields_width, level_size_fields_height = constants.game.LEVEL_1_SIZE
        sprite_width, sprite_height = constants.graphics.SPRITE_SIZE

        w, h = screen.get_size()

        h -= BOTTOM_UI_HEIGHT
        virtual_screen = pygame.surface.Surface((w, h))

        virtual_screen.blit(self.backdrop, (0, 0))

        tolerance_x = math.ceil(w / sprite_width)
        tolerance_y = math.ceil(h / sprite_height)

        filtered_layers = list(self.layers)

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
        z, y, x = self.search_character(constants.game.MAIN_CHARACTER_ID)

        if x < 0:
            x = 0

        if y < 0:
            y = 0

        self.camera_offset = [x, y]

    def handle_event(self, event):
        super().handle_event(event)

        
        if event.type == pygame.KEYUP and event.type == pygame.KEYUP and event.key in MOVEMENT_KEYS:
            self.moving = None
        elif event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            self.running = False

        if event.type == pygame.KEYDOWN:
            self.handle_keyboard_event(event)

    def handle_keyboard_event(self, event):
        if event.key == pygame.K_F5:
            utils.savegame.save_game(utils.savegame.QUICKSAVE, self.state)
        elif event.key == pygame.K_F9:
            utils.savegame.load_game(utils.savegame.QUICKSAVE, self.state)
        elif event.key in DISCARD_KEYS and self.state.player_state.show_detailed:
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

    def move_main_character(self, direction):
        z, y, x = self.search_character(constants.game.MAIN_CHARACTER_ID)
        character = self.layers[z][y][x]

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

        if (next_y > len(self.layers[z]) - 1):
            return

        if (next_x > len(self.layers[z][y]) - 1):
            return

        walkable = True
        layer_count = len(self.layers)

        for layer in range(0, layer_count):
            element = self.layers[layer][next_y][next_x]
            if element:
                element.handle_interact(character)

                if not element.walkable:
                    walkable = False

        if walkable:
            self.layers[z] = self.fill_fallback(None)
            self.layers[z][next_y][next_x] = character

            self.update_camera()

    def draw_headup(self, screen):
        self.state.player_state.draw(screen)
