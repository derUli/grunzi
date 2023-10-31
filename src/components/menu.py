import pygame
import os
import pygame_menu
import constants.game
import components.maingame
from utils.fps_counter import FPSCounter
from components.component import Component

class Menu(Component):

    def __init__(self, data_dir, handle_change_component):

        self.screen = None
        self.handle_change_component = handle_change_component
        self.menu = None

        self.skybox_image = pygame.image.load(
            os.path.join(data_dir, 'images', 'menu', 'sky.jpg')).convert()

        self.skybox_positions = [
            (0.0, 0.0),
            (float(self.skybox_image.get_width()), 0.0),
        ]

    def update_screen(self, screen):
        self.screen = screen
        self.draw_menu(self.screen)

    def start_the_game(self):
        self.handle_change_component(components.maingame.MainGame)

        self.menu.disable()

    def continue_game(self):
        self.start_the_game()

        # TODO load savegame

    def handle_event(self, event):
        return 

    def update_skybox(self):
        i = 0

        for skybox in self.skybox_positions:
            self.screen.blit(self.skybox_image, skybox)

            x, y = skybox

            if x < self.skybox_image.get_width() * -1.0:
                x = float(self.skybox_image.get_width())

            x -= 0.9

            self.skybox_positions[i] = (x, y)
            i += 1

    def draw_menu(self, screen):
        menu = pygame_menu.Menu(
            height=300,
            theme=pygame_menu.themes.THEME_BLUE,
            title='Welcome',
            width=400
        )

        menu.add.button('Play', self.start_the_game)
        menu.add.button('Continue', self.start_the_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu = menu
        menu.mainloop(screen, self.update_skybox)