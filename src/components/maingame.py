import pygame
import os
import pygame_menu
import constants.headup
import components.state.state
import utils.audio
from utils.fps_counter import FPSCounter
from components.component import Component

class MainGame(Component):
    def __init__(self, data_dir, handle_change_component):
        super().__init__(data_dir, handle_change_component)
        self.state = components.state.state.State(data_dir)

    def mount(self):
        atmo = 'level' + str(self.state.level) + '.ogg'
        self.play_music(atmo)

    def update_screen(self, screen):
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

