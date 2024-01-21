import os

from components.component import Component
from utils.animation import Animation
from utils.quality import filmgrain_enabled

FILMGRAIN_ALPHA = 60


class FilmGrain(Component):

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
            'filmgrain'
        )

        self.filmgrain = Animation(
            animation_dir,
            refresh_interval=0.13,
            start_frame=0,
            size=self.settings_state.screen_resolution
        )

    def draw_filmgrain(self, screen):
        """ Draw film grain """
        if not filmgrain_enabled():
            return

        grain = self.filmgrain.get_frame()
        grain.set_alpha(FILMGRAIN_ALPHA)
        screen.blit(grain, (0, 0))
