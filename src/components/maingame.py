import pygame
import os
import pygame_menu
import constants.headup
import constants.graphics
import constants.game
import components.state.state
import components.sprites.backdrop
import components.sprites.character
import components.menu
import components.sprites.raccoon
import pygame_menu
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
        self.menu = None

    def fill_layers(self):
        # Three layers
        self.layers = [
            self.fill_fallback(components.sprites.backdrop.Backdrop), # Backdrop layer
            self.fill_fallback(None), # Static objects
            self.fill_fallback(None), # Player character
        ]

        main_character = components.sprites.character.Character(self.sprites_dir)
        main_character.id = constants.game.MAIN_CHARACTER_ID
        
        self.layers[2][6][4] = main_character

        raccoon = components.sprites.raccoon.Raccoon(self.sprites_dir)

        
        self.layers[1][7][8] = raccoon


    def search_character(self, id):
        
        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if element and element.id == id:
                        return (z, y, x)

        return (0,0,0)

    def fill_fallback(self, callable):
         max_x = 10
         max_y = 10
         
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
            self.pause_menu()

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

        if(next_y < 0):
            return

        if(next_x < 0):
            return

        if(next_y > len(self.layers[z]) - 1):
            return

        if(next_x > len(self.layers[z][y]) - 1):
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
    
    def draw_headup(self, screen):
        self.state.player_state.draw_health(screen)
    

    def continue_game(self):
        self.menu.disable()

    def back_to_main_menu(self):
        self.continue_game()
        self.handle_change_component(components.menu.Menu)

    # Todo refactor to own class
    def pause_menu(self):
        menu = pygame_menu.Menu(
            height=300,
            theme=pygame_menu.themes.THEME_BLUE,
            title='Pause menu',
            width=400
        )

        menu.add.button('Continue', self.continue_game) # Continue game
        menu.add.button('Back To Main Menu', self.back_to_main_menu) # Return to main menu

        self.menu = menu
        menu.mainloop(self.screen)
        