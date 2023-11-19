""" Loading Screen """
import pygame

from components.component import Component
from constants.headup import BOTTOM_UI_BACKGROUND
from utils.quality import font_antialiasing_enabled


class LoadingScreen(Component):
    """ Loading screen component """

    def loading_screen(self, percentage=None, loading_text=None):
        """
        :param int percentage Loading percentage
        :param string Loading Text
        :rtype None
        """
        self.screen.fill(BOTTOM_UI_BACKGROUND)

        if not loading_text:
            loading_text = _('Loading...')

        # Show percentage if given
        if percentage is not None:
            percentage = str(int(percentage)) + "%"
            percentage = percentage.rjust(4, ' ')

            loading_text = ' '.join([loading_text, str(percentage)])

        # Render loading text
        rendered_text = self.monotype_font.render(
            loading_text,
            font_antialiasing_enabled(),
            (255, 255, 255)
        )

        # Calculate screen center
        pos_x, pos_y = self.screen.get_size()
        pos_x = pos_x / 2
        pos_y = pos_x / 2
        pos_x -= rendered_text.get_width() / 2
        pos_y -= rendered_text.get_height() / 2
        # draw text on screen
        self.screen.blit(rendered_text, (pos_x, pos_y))

        # Pump event queue and flip display to keep the application alive
        pygame.event.pump()
        pygame.display.update()
