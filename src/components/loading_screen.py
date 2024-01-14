""" Loading Screen """
import os

import pygame

from components.component import Component
from constants.headup import BOTTOM_UI_BACKGROUND, UI_MARGIN, PIGGY_PINK
from utils.quality import font_antialiasing_enabled

LOADING_BAR_COLOR = PIGGY_PINK


class LoadingScreen(Component):
    """ Loading screen component """

    def loading_screen(self, val=None, loading_text=None):
        """
        :param int percentage Loading percentage
        :param string Loading Text
        :rtype None
        """
        self.screen.fill(BOTTOM_UI_BACKGROUND)

        if not loading_text:
            loading_text = _('Loading...')

        # Show percentage if given
        if val is not None:
            percentage = str(int(val)) + "%"
            percentage = percentage.rjust(4, ' ')

            loading_text = ' '.join([loading_text, str(percentage)])

        # Render loading text
        rendered_text = self.monotype_font.render(
            loading_text,
            font_antialiasing_enabled(),
            LOADING_BAR_COLOR
        )

        backdrop = self.image_cache.load_image(
            os.path.join(
                self.data_dir,
                'images',
                'ui',
                'loading.jpg'
            ),
            self.screen.get_size()
        )

        h = rendered_text.get_height() + UI_MARGIN

        self.screen.blit(
            backdrop,
            (0, h),
            (0, 0,
             self.screen.get_width(),
             self.screen.get_height() - (h * 2)
             )
        )

        w = self.screen.get_width()
        onepercent_width = w / 100

        pos_x = 0
        pos_y = self.screen.get_height() - h

        current_width = onepercent_width * val

        if current_width > 0:
            surf = pygame.surface.Surface((current_width, h))

            surf.fill(LOADING_BAR_COLOR)
            self.screen.blit(surf, (pos_x, pos_y))

        # Calculate screen center
        pos_x, pos_y = self.screen.get_size()
        pos_x = pos_x / 2
        pos_x -= rendered_text.get_width() / 2
        pos_y = UI_MARGIN / 2

        # draw text on screen
        self.screen.blit(rendered_text, (pos_x, pos_y))

        # Pump event queue and flip display to keep the application alive
        pygame.event.pump()
        pygame.display.flip()
