import pygame
import os
import pygame_menu
import constants.headup
import constants.graphics
import constants.game
import components.state.state
import components.sprites.backdrop
import components.sprites.character
import utils.audio
from utils.fps_counter import FPSCounter
from components.component import Component
from constants.direction import *

class MainGame(Component):
    def __init__(self, data_dir, handle_change_component):
        super().__init__(data_dir, handle_change_component)
    
        self.state = components.state.state.State(self.data_dir)
        self.sprites_dir = os.path.join(self.data_dir, 'images', 'sprites')
        self.layers = []

    def fill_layers(self):
        # Three layers
        self.layers = [
            self.fill_fallback(components.sprites.backdrop.Backdrop),
            self.fill_fallback(None),
            self.fill_fallback(None),
        ]

        main_character = components.sprites.character.Character(self.sprites_dir)
        main_character.id = constants.game.MAIN_CHARACTER_ID

        self.layers[2][6][4] = main_character

    def search_character(self, id):
        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if element and element.id == id:
                        return (z, y, x)

        return None

    def fill_fallback(self, callable):
         max_x = 20
         max_y = 15
         
         rows = []

         for i in range(0, max_y):
            cols = []

            for n in range(0, max_x):
                s = None
                if callable:
                   s = callable(self.sprites_dir)
                cols.append(s)
            
            rows.append(cols)
        
         return rows

    def mount(self):
        atmo = 'level' + str(self.state.level) + '.ogg'
        self.play_music(atmo)

        self.fill_layers()

    def update_screen(self, screen):
        for layer in self.layers:
            y = 0
            x = 0
            for row in layer:
                for col in row:
                    if col:
                       col.draw(screen, x, y)
                    x += 1

                y+= 1
                x = 0

        self.draw_headup(screen)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            self.handle_keyboard_event(event)

    def handle_keyboard_event(self, event):
        if event.key == pygame.K_F3:
            self.state.player_state.hurt(10)
        elif event.key == pygame.K_ESCAPE:
            # Todo Pause menu instead of straight going to main menu
            self.handle_change_component(components.menu.Menu)

        elif event.key == pygame.K_LEFT:
            self.move_main_character(DIRECTION_LEFT)
        elif event.key == pygame.K_RIGHT:
            self.move_main_character(DIRECTION_RIGHT)
        elif event.key == pygame.K_UP:
            self.move_main_character(DIRECTION_UP)
        elif event.key == pygame.K_DOWN:
            self.move_main_character(DIRECTION_DOWN)

    def move_main_character(self, direction):
        z, y, x = self.search_character(constants.game.MAIN_CHARACTER_ID)

        character = self.layers[z][y][x]
        
        self.layers[z][y][z] = None
        character.change_direction(direction)

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

        if(next_y < 0):
            return

        if(next_x < 0):
            return

        if(next_y > len(self.layers[z])):
            return

        if(next_x > len(self.layers[z][y])):
            return

        # print(z, y, x, z, next_y, next_x)

        walkable = True
        layer_count = len(self.layers)

        for layer in range(0, layer_count):
            element = self.layers[layer][next_y][next_x]
            if element and not element.walkable:
                walkable = False
    
        if walkable:
            self.layers[z] = self.fill_fallback(None)
            self.layers[z][next_y][next_x] = character
    
    def draw_headup(self, screen):
        self.state.player_state.draw_health(screen)

