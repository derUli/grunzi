import os

from components.component import Component
from constants.headup import UI_MARGIN
from utils.animation import Animation


class LoadingIndicator(Component):

    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad
        )

        animation_dir = os.path.join(
            data_dir,
            'images',
            'sprites',
            'animations',
            'loading'
        )

        self.progress_indicator = Animation(
            animation_dir,
            refresh_interval=0.02,
            start_frame=0,
            size=(32, 32)
        )

        self.show_progress = False

    def draw_progress_indicator(self, screen):
        if not self.show_progress:
            return

        progress = self.progress_indicator.get_frame()

        w, h = progress.get_size()
        x = screen.get_width() - UI_MARGIN - h
        y = UI_MARGIN
        screen.blit(progress, (x, y))

    def change_progress_indicator(self, show_progress: bool):
        self.show_progress = show_progress
