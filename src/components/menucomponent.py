import os

from components.component import Component
from constants.headup import PIGGY_PINK
from utils.animation import Animation
from utils.helper import get_version


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

    def draw_background(self):
        """ Draw video background """
        video_frame = self.video.get_frame()
        if video_frame:
            self.screen.blit(video_frame, (0, 0))

        self.draw_notification(self.version_number, PIGGY_PINK, self.screen)

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
        component.video = self.video
        self.menu.disable()
