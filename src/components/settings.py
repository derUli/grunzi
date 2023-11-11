import gettext
import os

import pygame

from components.component import Component
from constants.headup import PIGGY_PINK
from constants.quality import QUALITY_LOW, QUALITY_MEDIUM, QUALITY_HIGH
from utils.animation import Animation
from utils.helper import get_version
from utils.menu import make_menu




class Settings(Component):
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

        version_file = os.path.join(self.data_dir, '..', 'VERSION')
        self.version_number = get_version(version_file)

    def update_screen(self, screen):
        self.draw_menu(self.screen)

    def handle_back(self):
        component = self.handle_change_component(None)
        component.video = self.video
        self.menu.disable()

    def draw_background(self):
        video_frame = self.video.get_frame()
        if video_frame:
            self.screen.blit(video_frame, (0, 0))
        self.draw_notification(self.version_number, PIGGY_PINK, self.screen)

        self.show_fps()

    def handle_change_limit_fps(self, selection, selected_index):
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.limit_fps = value
        self.settings_state.apply_and_save()

    def handle_change_screen_resolution(self, selection, selected_index):
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.screen_resolution = value
        self.settings_state.apply_and_save()

    def handle_show_fps(self):
        self.settings_state.show_fps = not self.settings_state.show_fps
        self.settings_state.apply_and_save()
        self.refresh_menu()

    def handle_change_music_volume(self, range_value):
        self.settings_state.music_volume = range_value / 100
        self.settings_state.apply_and_save()

    def handle_change_sound_volume(self, range_value):
        self.settings_state.sound_volume = range_value / 100
        self.settings_state.apply_and_save()

    def handle_toggle_fullscreen(self):
        self.settings_state.fullscreen = not self.settings_state.fullscreen
        self.settings_state.apply_and_save()
        self.refresh_menu()

    def handle_toggle_vsync(self):
        self.settings_state.vsync = not self.settings_state.vsync
        self.settings_state.apply_and_save()
        self.refresh_menu()

    def handle_change_quality(self, selection, selected_index):
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.quality = value
        self.settings_state.apply_and_save()
        self.video.reload()

    def get_fps_limit_items(self):
        return [
            (_('Unlimited'), 0),
            ('5', 5),
            ('20', 20),
            ('15', 15),
            ('30', 30),
            ('60', 60),
            ('120', 120),
            ('144', 144),
            ('240', 240),
        ]

    def get_quality_items(self):
        """ Get items for quality dropdown """
        return [
            (_('Low'), QUALITY_LOW),
            # Currently no selection because it isn't implemented yet
            (_('Medium'), QUALITY_MEDIUM),
            (_('High'), QUALITY_HIGH)
        ]

    def get_screen_resolution_items(self):
        modes = sorted(pygame.display.list_modes())
        items = []
        for x, y in modes:
            label = (str(x) + 'x' + str(y))
            value = (x, y)
            items.append((label, value))

        return items

    def get_selected_resolution_index(self):
        i = 0
        for label, value in self.get_screen_resolution_items():
            if value == self.settings_state.screen_resolution:
                continue

            i += 1

        return i

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
        menu = make_menu(_('Settings'), self.settings_state.limit_fps)

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
            placeholder_add_to_selection_box=False
        )

        menu.add.dropselect(
            title=_('Quality'),
            default=self.get_selected_index(self.get_quality_items(), self.settings_state.quality),
            items=self.get_quality_items(),
            onchange=self.handle_change_quality,
            placeholder_add_to_selection_box=False
        )

        # menu.add.dropselect(
        #     title=_('FPS Limit'),
        #     default=self.get_selected_index(self.get_fps_limit_items(), self.settings_state.limit_fps),
        #     items=self.get_fps_limit_items(),
        #     onchange=self.handle_change_limit_fps,
        #     placeholder_add_to_selection_box=False
        # )

        show_fps_text = _('Show FPS: ')

        if self.settings_state.show_fps:
            show_fps_text += _('On')
        else:
            show_fps_text += _('Off')

        # menu.add.button(show_fps_text, self.handle_show_fps)

        menu.add.range_slider(
            title=_('Music'),
            default=int(self.settings_state.music_volume * 100),
            range_values=(0, 100),
            increment=10,
            value_format=lambda x: str(int(x)) + "%",
            onchange=self.handle_change_music_volume
        )

        menu.add.range_slider(
            title=_('Sound Effects'),
            default=int(self.settings_state.sound_volume * 100),
            range_values=(0, 100),
            increment=10,
            value_format=lambda x: str(int(x)) + "%",
            onchange=self.handle_change_sound_volume
        )

        menu.add.button(_('Back To Main Menu'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
