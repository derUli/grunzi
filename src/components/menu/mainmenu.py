import pygame

import utils.savegame
from components.game.achievements import Achievements
from components.game.maingame import MainGame
from components.menu.loadgame import LoadGameComponent
from components.menu.menucomponent import MenuComponent
from components.settings.settings import Settings
from utils.menu import make_menu
from utils.savegame import get_latest_savegame


class MainMenu(MenuComponent):

    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad
        )

    def mount(self):
        if not pygame.mixer.music.get_busy():
            self.play_music('menu.ogg')

    def handle_new_game(self):
        component = self.handle_change_component(MainGame)
        if self.menu:
            self.menu.disable()

        component.new_game()

    def handle_load_game(self):
        component = self.handle_change_component(LoadGameComponent)
        component.x = self.x

        if self.menu:
            self.menu.disable()

    def handle_continue(self):

        if self.menu:
            self.menu.disable()

        component = self.handle_change_component(MainGame)
        component.load_savegame(get_latest_savegame())

    def handle_settings(self):
        """ Handle open settings menu  """
        component = self.handle_change_component(Settings)
        component.x = self.x
        self.menu.disable()

    def handle_achievements(self):
        """ Handle open settings menu  """
        self.handle_change_component(Achievements)
        self.menu.disable()

    def draw_menu(self, screen):
        """ Draw main menu """
        menu = make_menu(_('Grunzi'), self.settings_state.limit_fps)

        if get_latest_savegame():
            menu.add.button(_('Continue'), self.handle_continue)

        menu.add.button(_('New Game'), self.handle_new_game)

        if utils.savegame.has_savegames():
            menu.add.button(_('Load'), self.handle_load_game)  # Continue game

        menu.add.button(_('Achievements'), self.handle_achievements)


        menu.add.button(_('Settings'), self.handle_settings)

        menu.add.button(_('Quit'), self.quit_handler)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
