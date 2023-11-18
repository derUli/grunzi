""" Gamve Over Screen """
import os

import pygame

import utils.quality
from components.fadeable_component import FadeableComponent
from constants import gamepad
from constants import keyboard
from constants.game import MONOTYPE_FONT, LARGE_FONT_SIZE


class ToBeContinued(FadeableComponent):
    """ To be continued Screen """

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.menu = None

        self.monotype_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', MONOTYPE_FONT),
            LARGE_FONT_SIZE)

    def mount(self):
        self.fadein()

    def update_screen(self, screen):
        """ Update screen """
        if self.do_fade:
            screen = screen.copy().convert_alpha()
            screen.set_alpha(self.alpha)

        screen.fill((0, 0, 0))

        rendered_text = self.monotype_font.render(
            _('To be continued'),
            utils.quality.font_antialiasing_enabled(),
            (255, 255, 255)
        )

        pos_x, pos_y = self.screen.get_size()
        pos_x = pos_x / 2
        pos_y = pos_x / 2
        pos_x -= rendered_text.get_width() / 2
        pos_y -= rendered_text.get_height() / 2

        screen.blit(rendered_text, (pos_x, pos_y))

        self.draw_film_grain(screen)

        if self.do_fade:
            self.screen.blit(screen, (0, 0))

            self.fade()

    def handle_event(self, event):
        """ Handle events """
        if event.type == pygame.KEYDOWN and event.key in keyboard.CONFIRM_KEYS:
            self.handle_exit()
        elif event.type == pygame.JOYBUTTONDOWN and event.button == gamepad.K_CONFIRM:
            self.handle_exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_exit()

    def handle_exit(self):
        """ Back to main menu"""
        self.handle_change_component(None)
