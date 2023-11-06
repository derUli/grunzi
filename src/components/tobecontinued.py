""" Gamve Over Screen """
import gettext
import os

import pygame

from components.fadeable_component import FadeableComponent
from constants import gamepad
from constants import keyboard

_ = gettext.gettext

DISCARD_KEYS = keyboard.CONFIRM_KEYS + keyboard.ABORT_KEYS


class ToBeContinued(FadeableComponent):
    """ To be continued Screen """

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.menu = None

        file = os.path.join(data_dir, 'images', 'ui', 'to_be_continued.jpg')

        self.backdrop = self.image_cache.load_image(file)
        self.backdrop = pygame.transform.smoothscale(self.backdrop, settings_state.screen_resolution)

    def mount(self):
        self.fadein()

    def unmount(self):
        """ Show mouse on unmount and stop music """
        pygame.mouse.set_visible(1)
        pygame.mixer.music.stop()

    def draw_background(self, screen):
        """ Draw backdrop """
        screen.blit(self.backdrop, (0, 0))

    def update_screen(self, screen):
        surface = screen.copy().convert_alpha()
        surface.set_alpha(self.alpha)
        self.draw_background(surface)

        self.screen.blit(surface, (0, 0))

        self.fade()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in keyboard.DISCARD_KEYS:
            self.handle_exit()
        elif event.type == pygame.JOYBUTTONDOWN and event.button == gamepad.K_CONFIRM:
            self.handle_exit()

    def handle_exit(self):
        """ Back to main menu"""
        self.handle_change_component(None)
