import pygame_menu
import constants.game
import components.maingame
from components.component import Component
import utils.savegame
import gettext

_ = gettext.gettext

class Menu(Component):

    def __init__(self, data_dir, handle_change_component):
        """ Constructor """
        super().__init__(data_dir, handle_change_component)

        self.menu = None

    def mount(self):
        self.play_music('menu.ogg')

    def update_screen(self, screen):
        self.draw_menu(self.screen)

    def handle_new_game(self):
        self.handle_change_component(components.maingame.MainGame)
        self.menu.disable()

    def handle_continue_game(self):
        component = self.handle_change_component(components.maingame.MainGame)
        component.load_savegame()
        if self.menu:
            self.menu.disable()

    def draw_menu(self, screen):
        menu = pygame_menu.Menu(height=300,
                                theme=pygame_menu.themes.THEME_BLUE,
                                title=constants.game.WINDOW_CAPTION,
                                width=screen.get_width() / 3)

        menu.add.button(_('New Game'), self.handle_new_game)
        if utils.savegame.has_savegame(utils.savegame.DEFAULT_SAVE):
            menu.add.button(_('Continue'), self.handle_continue_game)  # Continue game

        menu.add.button(_('Quit'), pygame_menu.events.EXIT)

        self.menu = menu
        menu.mainloop(screen, self.update_skybox)
