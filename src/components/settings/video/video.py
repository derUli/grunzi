import pygame

from components.menucomponent import SettingsComponent
from components.settings.video.screen import SettingsScreen
from components.settings.video.graphics import SettingsGraphics

from constants.quality import QUALITY_OFF, QUALITY_MEDIUM, QUALITY_HIGH
from utils.menu import make_menu, get_longest_option
from utils.render_cache import store_clear


MIN_SCREEN_RESOLUTION = (800, 600)


class SettingsVideo(SettingsComponent):

    def draw_menu(self, screen):
        menu = make_menu(_('Video'), self.settings_state.limit_fps)

        menu.add.button(_('Screen'), self.handle_screen)
        menu.add.button(_('Graphics'), self.handle_graphics)

        menu.add.button(_('Back'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)


    def handle_screen(self):
        component = self.handle_change_component(SettingsScreen)
        component.video = self.video
        component.old_component = self
        self.menu.disable()

    def handle_graphics(self):
        component = self.handle_change_component(SettingsGraphics)
        component.video = self.video
        component.old_component = self
        self.menu.disable()