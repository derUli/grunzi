import os

import pygame
from PygameShader import scroll24

import utils.menu as menu
from components.component import Component
from constants.headup import PIGGY_PINK
from utils.helper import get_version
from utils.quality import font_antialiasing_enabled


class MenuComponent(Component):

    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad
        )

        self.backdrop = self.image_cache.load_image(
            os.path.join(self.data_dir, 'images', 'sprites', 'backdrops', 'menu.jpg'),
            settings_state.screen_resolution
        )
        self.menu = None
        self.old_component = None

        version_file = os.path.join(self.data_dir, '..', 'VERSION')
        self.version_number = get_version(version_file)
        self.apply_menu_fonts()
        self.x = 0

    def draw_background(self):
        """ Draw video background """
        backdrop = scroll24(self.backdrop, self.x, 0)
        self.screen.blit(backdrop, (0, 0))
        self.draw_notification(self.version_number, PIGGY_PINK, self.screen)
        self.x += 1

    def draw_menu(self, screen):
        pass

    def draw(self, screen):
        """ Draw """
        self.draw_menu(self.screen)

    def get_selected_index(self, items, selected):
        """ Get selected index for value """
        i = 0
        for item in items:
            text, value = item

            if value == selected:
                break

            i += 1

        return i

    def apply_menu_fonts(self):
        # Apply font to menus
        menu.THEME_PIG.title_font = pygame.font.Font(
            self.regular_font_file,
            menu.THEME_PIG.title_font_size
        )

        menu.THEME_PIG.widget_font = pygame.font.Font(
            self.regular_font_file,
            menu.THEME_PIG.widget_font_size
        )

        menu.THEME_PIG.title_font_antialias = font_antialiasing_enabled()
        menu.THEME_PIG.widget_font_antialias = font_antialiasing_enabled()


class SettingsComponent(MenuComponent):
    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad
        )

    def handle_back(self):
        """ Go back to settings menu """
        component = self.handle_change_component(self.old_component)
        component.x = self.x
        self.menu.disable()
