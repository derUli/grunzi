import os
import pygame

from components.menucomponent import SettingsComponent
from constants.quality import QUALITY_OFF, QUALITY_MEDIUM, QUALITY_HIGH
from utils.menu import make_menu, get_longest_option
from utils.render_cache import store_clear


MIN_SCREEN_RESOLUTION = (800, 600)

class SettingsGame(SettingsComponent):

    def handle_toggle_skip_intro(self, value):
        """ Handle toggle VSync """
        self.settings_state.skip_intro = value
        self.settings_state.apply_and_save()
        self.old_component.needs_restart = True

    def draw_menu(self, screen):
        menu = make_menu(_('Game'), self.settings_state.limit_fps)

        state_text = (_('No'), _('Yes'))

        menu.add.toggle_switch(
            _('Skip Intro'),
            self.settings_state.skip_intro,
            self.handle_toggle_skip_intro,
            state_text=state_text
        )

        menu.add.button(_('Back'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
