import pygame

from components.menu.menucomponent import SettingsComponent
from utils.menu import make_menu, get_longest_option

SCREEN_RESOLUTION_MIN = (1280, 720)


class SettingsScreen(SettingsComponent):
    def handle_change_screen_resolution(self, selection, selected_index):
        """ Handle change resolution """
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.screen_resolution = value
        self.settings_state.apply_and_save()
        self.settings_state.needs_restart = True

    def handle_toggle_fullscreen(self, value):
        """ Handle toggle fullscreen """
        self.settings_state.fullscreen = value
        self.settings_state.apply_and_save()

    def handle_toggle_vsync(self, value):
        """ Handle toggle VSync """
        self.settings_state.vsync = value
        self.settings_state.apply_and_save()
        self.settings_state.needs_restart = True

    def get_screen_resolution_items(self):
        """ Get screen resolution items """
        modes = pygame.display.list_modes()
        modes = list(filter(lambda item: item >= SCREEN_RESOLUTION_MIN, modes))

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

    def get_limit_fps(self):
        items = [
            (_('Uncapped'), 0)
        ]

        framerates = [
            144,
            120,
            60,
            30
        ]

        for fps in framerates:
            items.append(
                (
                    ' '.join([str(fps), 'FPS']),
                    fps
                )
            )

        return items

    def handle_change_limit_fps(self, selection, selected_index):
        """ Handle change limit fps """
        selected_item, index = selection
        text, value = selected_item
        self.settings_state.limit_fps = value
        self.settings_state.apply_and_save()

    def draw_menu(self, screen):
        menu = make_menu(_('Screen'), self.settings_state.limit_fps)

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
            title=_('Framerate Cap'),
            default=self.get_selected_index(
                self.get_limit_fps(),
                self.settings_state.limit_fps),
            items=self.get_limit_fps(),
            onchange=self.handle_change_limit_fps,
            placeholder_add_to_selection_box=False,
            placeholder=get_longest_option(self.get_limit_fps()),
        )

        menu.add.button(_('Back'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
