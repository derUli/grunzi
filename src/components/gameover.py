""" Gamve Over Screen """
import os
import gettext
import pygame
from utils.menu import make_menu
from components.component import Component
import utils.savegame
import utils.image

_ = gettext.gettext

class GameOver(Component):
    """ Gamve Over Screen """

    def __init__(self, data_dir, handle_change_component, settings_state):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state)
        self.menu = None

        file = os.path.join(data_dir, 'images', 'menu', 'gameover.jpg')

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
        self.screen.blit(self.backdrop, (0, 0))

    def update_screen(self, screen):
        """ Draw GameOver screen """
        self.backdrop = pygame.transform.smoothscale(
            self.backdrop, screen.get_size())

        menu = make_menu(_('Game Over'), screen)

        if utils.savegame.load_game(utils.savegame.DEFAULT_SAVE, self.settings_state):
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
