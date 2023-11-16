import logging
import os
import subprocess
import sys

import pygame

import constants.headup
from components.component import Component
from constants.headup import PIGGY_PINK
from constants.quality import QUALITY_VERY_LOW, QUALITY_LOW, QUALITY_MEDIUM, QUALITY_HIGH, QUALITY_VERY_HIGH
from utils.animation import Animation
from utils.helper import get_version
from utils.menu import make_menu, get_longest_option


class SettingsVideo(Component):
    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)

        video_path = os.path.join(
            data_dir,
            'images',
            'sprites',
            'animations',
            'dancing_pig'
        )

        # 25 Frames by second
        self.video = Animation(
            video_path,
            refresh_interval=1 / 25,
            size=self.settings_state.screen_resolution
        )

        self.menu = None
        self.old_component = None

        version_file = os.path.join(self.data_dir, '..', 'VERSION')
        self.version_number = get_version(version_file)

    def update_screen(self, screen):
        self.draw_menu(self.screen)

    def handle_back(self):
        component = self.handle_change_component(self.old_component)
        component.video = self.video
        self.menu.disable()

    def draw_background(self):
        if self.settings_state.quality >= QUALITY_LOW:
            video_frame = self.video.get_frame()
            if video_frame:
                self.screen.blit(video_frame, (0, 0))

        self.draw_notification(self.version_number, PIGGY_PINK, self.screen)

    def handle_change_limit_fps(self, selection, selected_index):
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.limit_fps = value
        self.settings_state.apply_and_save()

    def handle_change_screen_resolution(self, selection, selected_index):
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.screen_resolution = value
        self.old_component.needs_restart = True
        self.settings_state.apply_and_save()

    def handle_toggle_fullscreen(self):
        self.settings_state.fullscreen = not self.settings_state.fullscreen
        self.settings_state.apply_and_save()
        self.refresh_menu()

    def handle_toggle_vsync(self):
        self.settings_state.vsync = not self.settings_state.vsync
        self.settings_state.apply_and_save()
        self.old_component.needs_restart = True
        self.refresh_menu()

    def handle_change_quality(self, selection, selected_index):
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.quality = value
        self.settings_state.apply_and_save()
        self.video.reload()

    def get_quality_items(self):
        """ Get items for quality dropdown """
        return [
            (_('Very Low'), QUALITY_VERY_LOW),
            (_('Low'), QUALITY_LOW),
            (_('Medium'), QUALITY_MEDIUM),
            (_('High'), QUALITY_HIGH),
            (_('Very High'), QUALITY_VERY_HIGH),
        ]

    def handle_dummy(self):
        """ Dummy handler does nothing """
        return

    def get_screen_resolution_items(self):
        """ Get screen resolution items """
        modes = pygame.display.list_modes()

        # If the current screen resolution is not in supported modes add it
        if self.settings_state.screen_resolution not in modes:
            modes.append(self.settings_state.screen_resolution)

        modes = sorted(modes)

        items = []
        for x, y in modes:
            label = (str(x) + 'x' + str(y))
            value = (x, y)
            items.append((label, value))

        return items

    def get_selected_index(self, items, selected):
        i = 0
        for item in items:
            text, value = item

            if value == selected:
                break

            i += 1

        return i

    def refresh_menu(self):
        self.menu.disable()
        self.draw_menu(self.screen)

    def draw_menu(self, screen):
        menu = make_menu(_('Video'), self.settings_state.limit_fps)

        w = menu.get_width() - (constants.headup.UI_MARGIN * 2)

        fullscreen_text = _('Display Mode: ')

        if self.settings_state.fullscreen:
            fullscreen_text += _('Fullscreen')
        else:
            fullscreen_text += _('Window')

        menu.add.button(fullscreen_text, self.handle_toggle_fullscreen)

        vsync_text = _('V-Sync: ')

        if self.settings_state.vsync:
            vsync_text += 'On'
        else:
            vsync_text += 'Off'

        menu.add.button(vsync_text, self.handle_toggle_vsync)

        menu.add.dropselect(
            title=_('Screen Resolution'),
            default=self.get_selected_index(self.get_screen_resolution_items(), self.settings_state.screen_resolution),
            items=self.get_screen_resolution_items(),
            onchange=self.handle_change_screen_resolution,
            placeholder_add_to_selection_box=False,
            placeholder=get_longest_option(self.get_screen_resolution_items()),
        )

        menu.add.dropselect(
            title=_('Quality'),
            default=self.get_selected_index(self.get_quality_items(), self.settings_state.quality),
            items=self.get_quality_items(),
            onchange=self.handle_change_quality,
            placeholder_add_to_selection_box=False,
            placeholder=get_longest_option(self.get_quality_items()),
        )

        menu.add.button(_('Back'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
