""" Achievements Screen """
import os

import pygame

import utils.quality
from components.mixins.filmgrain import FilmGrain
from constants import gamepad
from constants import keyboard
from constants.game import REGULAR_FONT, LARGE_FONT_SIZE
from state.achievements import AchievementsState


class Achievements(FilmGrain):
    """ Achievements Screen """

    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad)
        self.regular_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', REGULAR_FONT),
            LARGE_FONT_SIZE)

        self.rendered_text = None

        self.backdrop = None
        self.state = AchievementsState()

    def mount(self):
        self.state.load()

    def draw(self, screen):
        """ Update screen """

        if not self.backdrop:
            file = os.path.join(
                self.data_dir,
                'images',
                'ui',
                'schoolboard.jpg')
            self.backdrop = self.image_cache.load_image(
                file, screen.get_size())

        self.screen.blit(self.backdrop, (0, 0))

        if not self.rendered_text:
            self.rendered_text = self.regular_font.render(
                _('Coming Soon'),
                utils.quality.font_antialiasing_enabled(),
                (255, 255, 255)
            )

        pos_x, pos_y = self.screen.get_size()
        pos_x = pos_x / 2
        pos_y = pos_x / 2
        pos_x -= self.rendered_text.get_width() / 2
        pos_y -= self.rendered_text.get_height() / 2

        screen.blit(self.rendered_text, (pos_x, pos_y))

        self.draw_filmgrain(screen)

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
