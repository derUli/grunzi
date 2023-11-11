""" Gamve Over Screen """
import os

import pygame

import utils.image
import utils.quality
import utils.savegame
from components.component import Component
from constants.quality import QUALITY_LOW
from utils.menu import make_menu


class GameOver(Component):
    """ Gamve Over Screen """

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.menu = None

        file = os.path.join(data_dir, 'images', 'ui', 'gameover.jpg')

        self.backdrop = self.image_cache.load_image(file)

    def mount(self):
        """ Play game over music once """
        # CREDITS: https://audionautix.com/creative-commons-music
        self.play_music('gameover.ogg', 0)

    def unmount(self):
        """ Show mouse on unmount and stop music """
        pygame.mouse.set_visible(1)
        pygame.mixer.music.stop()

    def draw_background(self):
        """ Draw backdrop """
        if self.settings_state.quality >= QUALITY_LOW:
            self.screen.blit(self.backdrop, (0, 0))

        self.draw_film_grain(self.screen)
        self.show_fps()

    def update_screen(self, screen):
        """ Draw GameOver screen """
        self.backdrop = utils.quality.scale_method()(
            self.backdrop, screen.get_size())

        menu = make_menu(_('Game Over'), self.settings_state.limit_fps)

        if utils.savegame.has_savegame(utils.savegame.DEFAULT_SAVE):
            menu.add.button(_('Load Game'), self.handle_load_game)  # Load save game
        menu.add.button(_('Back To Main Menu'),
                        self.handle_back_to_main_menu)  # Return to main menu

        self.menu = menu
        menu.mainloop(self.screen, self.draw_background)

    def handle_load_game(self):
        """ On click 'Load Game' """
        self.menu.disable()
        component = self.handle_change_component(None)
        component.handle_continue_game()

    def handle_back_to_main_menu(self):
        """ On click 'Back To Main Menu' """
        self.menu.disable()
        self.handle_change_component(None)
