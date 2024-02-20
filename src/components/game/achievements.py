""" Achievements Screen """
import os

import pygame

import utils.quality
from components.mixins.filmgrain import FilmGrain
from components.settings.controls import HORIZONTAL_MARGIN, FONT_SIZE, LINE_LARGE_MARGIN
from constants import gamepad
from constants import keyboard
from constants.game import REGULAR_FONT, LARGE_FONT_SIZE
from state.achievements import AchievementsState

TEXT_COLOR = (255, 255, 255)


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

        self.backdrop = None
        fontfile = os.path.join(data_dir, 'fonts', REGULAR_FONT)
        self.font = pygame.font.Font(
            fontfile,
            FONT_SIZE
        )

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

        screen.blit(self.backdrop, (0, 0))

        x = HORIZONTAL_MARGIN
        y = HORIZONTAL_MARGIN

        rendered_text = self.font.render(
            _('Errungenschaften'),
            utils.quality.font_antialiasing_enabled(),
            pygame.Color(TEXT_COLOR)
        )

        screen.blit(rendered_text, (x, y))

        y += rendered_text.get_height()
        y += LINE_LARGE_MARGIN

        for achievement in self.state.achievements:
            rendered_text = self.font.render(
                self.state.achievements[achievement].get_display_text(),
                utils.quality.font_antialiasing_enabled(),
                pygame.Color(TEXT_COLOR)
            )

            screen.blit(rendered_text, (x, y))

            x = screen.get_width() - HORIZONTAL_MARGIN

            file = os.path.join(self.data_dir, 'images', 'ui', 'check.png')

            image = self.image_cache.load_image(
                file, (rendered_text.get_height(), rendered_text.get_height())
            )

            if not self.state.achievements[achievement].completed:
                image = pygame.transform.grayscale(image)

            screen.blit(image, (x, y))

            x = HORIZONTAL_MARGIN
            y += rendered_text.get_height()
            y += LINE_LARGE_MARGIN

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
