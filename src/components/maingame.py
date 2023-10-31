import pygame
import os
import pygame_menu
import constants.headup
import constants.graphics
import components.state.state
import components.sprites.gras
import utils.audio
from utils.fps_counter import FPSCounter
from components.component import Component

class MainGame(Component):
    def __init__(self, data_dir, handle_change_component):
        super().__init__(data_dir, handle_change_component)
    
        self.state = components.state.state.State(self.data_dir)
        self.sprites_dir = os.path.join(self.data_dir, 'images', 'sprites')
        self.layers = []

    def fill_layers(self):
        # Three layers
        self.layers = [
            [],
            [],
            []
        ]


        self.fill_gras_fallback()


    def fill_gras_fallback(self):
         max_x = 20
         max_y = 15
         
         sprite = components.sprites.gras.Gras(self.sprites_dir)

         for i in range(0, max_y):
            row = []

            for n in range(0, max_x):
                row.append(sprite)
            
            self.layers[0].append(row)

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
    
    def draw_headup(self, screen):
        self.state.player_state.draw_health(screen)

