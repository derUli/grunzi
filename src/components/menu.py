import os

import pygame
import pygame_menu

import utils.savegame
from components.settings_component import SettingsComponent
from components.intro import Intro
from components.maingame import MainGame
from components.settings import Settings
from constants.headup import PIGGY_PINK
from utils.animation import Animation
from utils.helper import get_version
from utils.menu import make_menu


class Menu(SettingsComponent):

    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad)

    def mount(self):
        if not pygame.mixer.music.get_busy():
            self.play_music('menu.ogg')

    def handle_new_game(self):
        self.handle_change_component(Intro)
        if self.menu:
            self.menu.disable()

    def handle_continue_game(self):
        component = self.handle_change_component(MainGame)
        if self.menu:
            self.menu.disable()
        component.load_savegame()

    def handle_settings(self):
        """ Handle open settings menu  """
        component = self.handle_change_component(Settings)
        component.video = self.video
        self.menu.disable()

    def draw_menu(self, screen):
        """ Draw main menu """
        menu = make_menu(_('Grunzi'), self.settings_state.limit_fps)
        menu.add.button(_('New Game'), self.handle_new_game)
        if utils.savegame.has_savegame(utils.savegame.DEFAULT_SAVE):
            menu.add.button(
                _('Continue'),
                self.handle_continue_game)  # Continue game

        menu.add.button(_('Settings'), self.handle_settings)

        menu.add.button(_('Quit'), pygame_menu.events.EXIT)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
