import logging
import subprocess
import sys

import pygame

from components.menu.menucomponent import MenuComponent
from components.settings.audio import SettingsAudio
from components.settings.controls import SettingsControls
from components.settings.video.video import SettingsVideo
from utils.menu import make_menu


class Settings(MenuComponent):
    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad
        )

    def handle_back(self):
        """ Go back to main menu """
        if self.settings_state.needs_restart:
            self.restart_app()
            return
        component = self.handle_change_component(None)
        component.x = self.x
        self.menu.disable()

    def restart_app(self):
        """ Restart game """
        pygame.quit()
        logging.debug('Restart application to apply settings')

        command = [sys.executable] + sys.argv

        # If we are running from Exe
        if getattr(sys, "frozen", False):
            command = sys.argv

        with subprocess.Popen(command):
            sys.exit()

    def handle_video(self):
        component = self.handle_change_component(SettingsVideo)
        component.x = self.x
        component.old_component = self
        self.menu.disable()

    def handle_audio(self):
        component = self.handle_change_component(SettingsAudio)
        component.x = self.x
        component.old_component = self
        self.menu.disable()

    def handle_controls(self):
        """ Handle open settings menu  """
        component = self.handle_change_component(SettingsControls)
        component.old_component = self

        self.menu.disable()

    def draw_menu(self, screen):
        menu = make_menu(_('Settings'), self.settings_state.limit_fps)

        menu.add.button(_('Video'), self.handle_video)
        menu.add.button(_('Audio'), self.handle_audio)
        menu.add.button(_('Controls'), self.handle_controls)
        menu.add.button(_('Back To Main Menu'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
