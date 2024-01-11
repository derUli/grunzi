import os
import pygame

from components.component import Component
from constants.headup import PIGGY_PINK
from constants.quality import QUALITY_OFF, QUALITY_MEDIUM, QUALITY_HIGH
from utils.animation import Animation
from utils.helper import get_version
from utils.menu import make_menu, get_longest_option
from utils.render_cache import store_clear
import math


MIN_SCREEN_RESOLUTION = (1280, 720)


def calculate_aspect(width: int, height: int) -> str:
    r = math.gcd(width, height)
    x = int(width / r)
    y = int(height / r)
    return f"{x}:{y}"


class SettingsVideo(Component):
    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad)

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

    def draw(self, screen):
        """ Draw """
        self.draw_menu(self.screen)

    def handle_back(self):
        """ Go back to settings menu """
        component = self.handle_change_component(self.old_component)
        component.video = self.video
        self.menu.disable()

    def draw_background(self):
        """ Draw video background """
        video_frame = self.video.get_frame()
        if video_frame:
            self.screen.blit(video_frame, (0, 0))

        self.draw_notification(self.version_number, PIGGY_PINK, self.screen)

    def handle_change_screen_resolution(self, selection, selected_index):
        """ Handle change resolution """
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.screen_resolution = value
        self.old_component.needs_restart = True
        self.settings_state.apply_and_save()
        store_clear()

    def handle_toggle_fullscreen(self, value):
        """ Handle toggle fullscreen """
        self.settings_state.fullscreen = value
        self.settings_state.apply_and_save()

    def handle_toggle_vsync(self, value):
        """ Handle toggle VSync """
        self.settings_state.vsync = value
        self.settings_state.apply_and_save()
        self.old_component.needs_restart = True

    def get_screen_resolution_items(self):
        """ Get screen resolution items """
        modes = pygame.display.list_modes()

        # If the current screen resolution is not in supported modes add it
        if self.settings_state.screen_resolution not in modes:
            modes.append(self.settings_state.screen_resolution)

        modes = sorted(modes)

        items = []
        for x, y in modes:
            # Screen resolutions lower than this would crash
            if (x, y) < MIN_SCREEN_RESOLUTION:
                continue

            label = (str(x) + 'x' + str(y))
            value = (x, y)
            items.append((label, value))

        return items

    def get_blood_items(self):
        return [
            (_('Off'), QUALITY_OFF),
            (_('Medium'), QUALITY_MEDIUM),
            (_('High'), QUALITY_HIGH),
        ]

    def handle_change_blood(self, selection, selected_index):
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.blood = value
        self.settings_state.apply_and_save()

    def handle_toggle_bloom(self, value):
        """ Handle toggle bloom """
        self.settings_state.bloom = value
        self.settings_state.apply_and_save()

    def handle_toggle_smoothscale(self, value):
        """ Handle toggle bloom """
        self.settings_state.smoothscale = value
        self.settings_state.apply_and_save()

    def handle_toggle_fog(self, value):
        """ Handle toggle fog """
        self.settings_state.fog = value
        self.settings_state.apply_and_save()

    def get_selected_index(self, items, selected):
        """ Get selected index for value """
        i = 0
        for item in items:
            text, value = item

            if value == selected:
                break

            i += 1

        return i

    def draw_menu(self, screen):
        menu = make_menu(_('Video'), self.settings_state.limit_fps)

        state_text = (_('Off'), _('On'))

        menu.add.toggle_switch(
            _('Fullscreen'),
            self.settings_state.fullscreen,
            self.handle_toggle_fullscreen,
            state_text=state_text
        )

        menu.add.toggle_switch(
            _('V-Sync'),
            self.settings_state.vsync,
            self.handle_toggle_vsync,
            state_text=state_text
        )

        menu.add.dropselect(
            title=_('Screen Resolution'),
            default=self.get_selected_index(
                self.get_screen_resolution_items(),
                self.settings_state.screen_resolution),
            items=self.get_screen_resolution_items(),
            onchange=self.handle_change_screen_resolution,
            placeholder_add_to_selection_box=False,
            placeholder=get_longest_option(self.get_screen_resolution_items()),
        )

        menu.add.dropselect(
            title=_('Blood'),
            default=self.get_selected_index(
                self.get_blood_items(),
                self.settings_state.blood),
            items=self.get_blood_items(),
            onchange=self.handle_change_blood,
            placeholder_add_to_selection_box=False,
            placeholder=get_longest_option(self.get_blood_items()),
        )

        menu.add.toggle_switch(
            _('Fog'),
            self.settings_state.fog,
            self.handle_toggle_fog,
            state_text=state_text
        )

        menu.add.toggle_switch(
            _('Bloom'),
            self.settings_state.bloom,
            self.handle_toggle_bloom,
            state_text=state_text
        )

        menu.add.toggle_switch(
            _('Smooth Scale'),
            self.settings_state.smoothscale,
            self.handle_toggle_smoothscale,
            state_text=state_text
        )

        menu.add.button(_('Back'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
