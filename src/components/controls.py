""" Gamve Over Screen """
import os

import pygame

import utils.quality
from components.fadeable_component import FadeableComponent
from constants import gamepad
from constants import keyboard
from constants.game import MONOTYPE_FONT
from constants.quality import QUALITY_LOW

PAGE_KEYBOARD = 0
PAGE_CONTROLLER = 1

TEXT_COLOR = (255, 255, 255)
LINE_SMALL_MARGIN = 20
LINE_LARGE_MARGIN = 28
HORIZONTAL_MARGIN = 45

FONT_SIZE = 28


class Controls(FadeableComponent):
    """ Controls screen """

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.menu = None

        self.current_page = PAGE_KEYBOARD

        file = os.path.join(data_dir, 'images', 'ui', 'schoolboard.jpg')

        self.backdrop = self.image_cache.load_image(file, self.settings_state.screen_resolution)

        fontfile_headline = os.path.join(data_dir, 'fonts', MONOTYPE_FONT)
        self.font = pygame.font.Font(
            fontfile_headline,
            FONT_SIZE
        )

    def keyboard_controls(self):
        return [
            (_('Walk'), 'Arrow_Keys.png'),
            (_('Use item'), 'E_Key_Dark.png'),
            (_('Drop item'), 'Z_Key_Dark.png'),
            (_('Grunt'), 'G_Key_Dark.png'),
            (_('Run'), 'Shift_Key_Dark.png'),
            (_('Pause'), 'Esc_Key_Dark.png'),
            (_('Make Screenshot'), 'F12_Key_Dark.png'),
        ]

    def controller_controls(self):
        return [
            (_('Walk'), '360_Dpad.png'),
            (_('Use item'), '360_A.png'),
            (_('Drop item'), '360_Y.png'),
            (_('Grunt'), '360_X.png'),
            (_('Run'), '360_RT.png'),
            (_('Pause'), '360_Start.png'),
        ]

    def mount(self):
        self.fadein()

    def update_screen(self, screen):
        """ Update screen """
        surface = screen.copy().convert_alpha()
        surface.set_alpha(self.alpha)

        if self.settings_state.quality >= QUALITY_LOW:
            surface.blit(self.backdrop, (0, 0))
        controls_text = self.font.render(
            _('Controls'),
            utils.quality.font_antialiasing_enabled(),
            pygame.Color(TEXT_COLOR)
        )

        x = HORIZONTAL_MARGIN
        y = HORIZONTAL_MARGIN
        surface.blit(controls_text, (x, y))

        y += controls_text.get_height()
        y += LINE_LARGE_MARGIN

        controls = []

        if self.current_page == PAGE_KEYBOARD:
            controls = self.keyboard_controls()
        elif self.current_page == PAGE_CONTROLLER:
            controls = self.controller_controls()

        for control in controls:
            label, image_file = control

            control_text = self.font.render(
                label,
                utils.quality.font_antialiasing_enabled(),
                pygame.Color(TEXT_COLOR)
            )

            surface.blit(control_text, (x, y))

            image_path = os.path.join(self.data_dir, 'images', 'ui', 'controls', image_file)
            scale_to = (control_text.get_height(), control_text.get_height())
            if image_file == 'Arrow_Keys.png':
                scale_to = (156, control_text.get_height())

            image = self.image_cache.load_image(
                image_path,
                scale_to
            )

            pos_image = (
                surface.get_width() - HORIZONTAL_MARGIN - image.get_width(),
                y
            )

            surface.blit(image, pos_image)

            y += controls_text.get_height()
            y += LINE_SMALL_MARGIN

        self.draw_film_grain(surface)
        screen.blit(surface, (0, 0))

        self.fade()

    def handle_event(self, event):
        """ Handle events """
        if event.type == pygame.KEYDOWN and event.key in keyboard.CONFIRM_KEYS:
            self.next_page()
        elif event.type == pygame.JOYBUTTONDOWN and event.button == gamepad.K_CONFIRM:
            self.next_page()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.next_page()

    def next_page(self):
        if self.current_page == PAGE_KEYBOARD:
            if self.gamepad:
                self.current_page = PAGE_CONTROLLER
            else:
                self.handle_change_component(None)
        elif self.current_page == PAGE_CONTROLLER:
            """ Back to main menu"""
            self.handle_change_component(None)
