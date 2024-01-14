""" Gamve Over Screen """
import os

import pygame

import components.menu.loadgame
import utils.image
import utils.quality
import utils.savegame
from components.mixins.filmgrain import FilmGrain
from utils.menu import make_menu


class GameOver(FilmGrain):
    """ Gamve Over Screen """

    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad)
        self.menu = None

        self.backdrop = self.image_cache.load_image(
            os.path.join(
                data_dir,
                'images',
                'ui',
                'gameover.jpg'
            ),
            self.settings_state.screen_resolution
        )

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
        self.screen.blit(self.backdrop, (0, 0))

        self.draw_filmgrain(self.screen)

    def draw(self, screen):
        """ Draw GameOver screen """

        menu = make_menu(_('Game Over'), self.settings_state.limit_fps)

        if utils.savegame.has_savegames():
            menu.add.button(_('Load Game'),
                            self.handle_load_game)  # Load save game
        menu.add.button(_('Back To Main Menu'),
                        self.handle_back_to_main_menu)  # Return to main menu

        self.menu = menu
        menu.mainloop(self.screen, self.draw_background)

    def handle_load_game(self):
        """ On click 'Load Game' """
        self.menu.disable()
        self.handle_change_component(components.menu.loadgame.LoadGameComponent)

    def handle_back_to_main_menu(self):
        """ On click 'Back To Main Menu' """
        self.menu.disable()
        self.handle_change_component(None)
