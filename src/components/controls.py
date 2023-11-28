""" Controls Screen """
import os

import pygame

import utils.quality
from components.fadeable_component import FadeableComponent
from constants import gamepad
from constants import keyboard
from constants.game import MONOTYPE_FONT
from constants.quality import QUALITY_LOW
from utils.string import label_value

PAGE_KEYBOARD = 0
PAGE_CONTROLLER = 1
PAGE_MOUSE = 2

TEXT_COLOR = (255, 255, 255)
LINE_SMALL_MARGIN = 20
LINE_LARGE_MARGIN = 28
HORIZONTAL_MARGIN = 90

FONT_SIZE = 28

SUPPORTED_CONTROLLERS = [
    'Xbox 360 Controller'
]


class Controls(FadeableComponent):
    """ Controls screen """

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.menu = None

        self.current_page = PAGE_KEYBOARD
        self.old_component = None
        self.data_dir = data_dir
        self.backdrop = None
        self.enable_mouse = False

        fontfile = os.path.join(data_dir, 'fonts', MONOTYPE_FONT)
        self.font = pygame.font.Font(
            fontfile,
            FONT_SIZE
        )

    def keyboard_controls(self):
        """ Get keyboard controls """
        return [
            (_('Walk'), 'Arrow_Keys.png'),
            (_('Use item'), 'E_Key_Dark.png'),
            (_('Drop item'), 'Q_Key_Dark.png'),
            (_('Grunt'), 'G_Key_Dark.png'),
            (_('Run'), 'Shift_Key_Dark.png'),
            (_('Pause'), 'Esc_Key_Dark.png'),
            (_('Make Screenshot'), 'F12_Key_Dark.png'),
        ]

    def controller_controls(self):
        """ Get controller controls """
        return [
            (_('Walk'), '360_Dpad.png'),
            (_('Use item'), '360_A.png'),
            (_('Drop item'), '360_Y.png'),
            (_('Grunt'), '360_X.png'),
            (_('Run'), '360_RT.png'),
            (_('Pause'), '360_Start.png'),
        ]

    def mouse_controls(self):
        """ Get mouse controls """
        controls = [(_('Experimental mouse support'), None)]

        state_text = _('Disabled')

        mouse_enabled = self.enable_mouse

        if mouse_enabled:
            state_text = _('Enabled')

        controls.append((label_value(_('Status'), state_text), None))

        if not mouse_enabled:
            controls.append(
                (
                    _('To enable the experimental mouse support run the game with'), None
                )
            )
            controls.append(
                (
                    _('the --enable-mouse flag.'), None
                )
            )

        return controls

    def mount(self):
        """ Fade in on mount """
        self.fadein()

    def unmount(self):
        """ Do nothing on unmount """
        return

    def draw(self, screen):
        """ Update screen """
        if not self.backdrop:
            file = os.path.join(self.data_dir, 'images', 'ui', 'schoolboard.jpg')
            self.backdrop = self.image_cache.load_image(file, screen.get_size())

        if self.do_fade:
            surface = screen.copy().convert_alpha()
            surface.set_alpha(self.alpha)
        else:
            surface = screen

        if self.settings_state.quality >= QUALITY_LOW:
            surface.blit(self.backdrop, (0, 0))
        else:
            surface.fill((0, 0, 0))

        headline = _('Controls')

        headline += ' ('
        if self.current_page == PAGE_KEYBOARD:
            headline += _('Keyboard')
        elif self.current_page == PAGE_CONTROLLER:
            headline += _('Controller')
        elif self.current_page == PAGE_MOUSE:
            headline += _('Mouse')

        headline += ')'

        controls_text = self.font.render(
            headline,
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
        elif self.current_page == PAGE_MOUSE:
            controls = self.mouse_controls()

        for control in controls:
            label, image_file = control

            control_text = self.font.render(
                label,
                utils.quality.font_antialiasing_enabled(),
                pygame.Color(TEXT_COLOR)
            )

            surface.blit(control_text, (x, y))

            if not image_file:
                y += controls_text.get_height()
                y += LINE_SMALL_MARGIN
                continue

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

        text = _('Controller: ')

        if self.gamepad and self.gamepad.joystick:
            controller_name = self.gamepad.joystick.get_name()
            text += controller_name

            if controller_name not in SUPPORTED_CONTROLLERS:
                text += ' (' + _('Unsupported') + ')'
        else:
            text += _('No Controller')

        control_text = self.font.render(
            text,
            utils.quality.font_antialiasing_enabled(),
            pygame.Color(TEXT_COLOR)
        )

        y = screen.get_height() - controls_text.get_height() - HORIZONTAL_MARGIN

        if self.current_page == PAGE_CONTROLLER:
            surface.blit(control_text, (x, y))

        self.draw_film_grain(surface)

        if self.do_fade:
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
        """ Turn next page """
        if self.current_page == PAGE_KEYBOARD:
            self.current_page = PAGE_CONTROLLER
        elif self.current_page == PAGE_CONTROLLER:
            self.current_page = PAGE_MOUSE
        else:
            #  Back to settings menu
            self.handle_change_component(self.old_component)
