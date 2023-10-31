import pygame
import os
import pygame_menu
import constants.headup
import constants.graphics
import constants.game
import components.state.state
import components.sprites.backdrop
import components.sprites.sprite
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
            self.fill_fallback(components.sprites.backdrop.Backdrop(self.sprites_dir)),
            self.fill_fallback(components.sprites.sprite.Sprite(self.sprites_dir)),
            self.fill_fallback(components.sprites.sprite.Sprite(self.sprites_dir))
        ]

        main_character =  components.sprites.character.Character(self.sprites_dir)
        main_character.id = constants.game.MAIN_CHARACTER_ID

        self.layers[2][9][7] = main_character

    def search_character(self, id):
        z = 0
    
        for layer in self.layers:
            x = 0
            y = 0
            for row in layer:

                for col in row:
                    print(col.id, id)
                    if(col.id == id):
                        return (z, y, x)
                    x += 1
                x = 0
                y += 1
            
            z+= 1

        return None

    def fill_fallback(self, sprite):
         max_x = 20
         max_y = 15
         
         layer = []

         for i in range(0, max_y):
            row = []

            for n in range(0, max_x):
                row.append(sprite)
            
            layer.append(row)
        
         return layer

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
        
        self.layers[z][y][x].change_direction(direction)
        

    
    def draw_headup(self, screen):
        self.state.player_state.draw_health(screen)

