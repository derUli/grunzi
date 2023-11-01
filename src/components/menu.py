import pygame
import pygame_menu
import constants.game
import components.maingame
from components.component import Component
import utils.savegame


class Menu(Component):

    def __init__(self, data_dir, handle_change_component):
        """ Constructor """
        super().__init__(data_dir, handle_change_component)

        self.menu = None

    def mount(self):
        self.play_music('menu.ogg')

    def update_screen(self, screen):
        self.draw_menu(self.screen)

    def start_the_game(self):
        self.handle_change_component(components.maingame.MainGame)
        self.menu.disable()

    def continue_game(self):
        component = self.handle_change_component(components.maingame.MainGame)
        component.load_savegame()
        if self.menu:
            self.menu.disable()

    def draw_menu(self, screen):
        menu = pygame_menu.Menu(height=300,
                                theme=pygame_menu.themes.THEME_BLUE,
                                title=constants.game.WINDOW_CAPTION,
                                width=400)

        menu.add.button('Play', self.start_the_game)
        if utils.savegame.has_savegame(utils.savegame.DEFAULT_SAVE):
            menu.add.button('Continue', self.continue_game)  # Continue game

        menu.add.button('Quit', pygame_menu.events.EXIT)

        self.menu = menu
        menu.mainloop(screen, self.update_skybox)
