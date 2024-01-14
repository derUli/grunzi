""" Loading Screen """
import pygame

from components.component import Component
from constants.headup import BOTTOM_UI_BACKGROUND, UI_MARGIN
from utils.quality import font_antialiasing_enabled

LOADING_COLOR = (255, 255, 255)

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
            LOADING_COLOR
        )

        # Calculate screen center
        pos_x, pos_y = self.screen.get_size()
        pos_x = pos_x / 2
        pos_y = pos_x / 2
        pos_x -= rendered_text.get_width() / 2
        pos_y -= rendered_text.get_height() / 2
        # draw text on screen
        self.screen.blit(rendered_text, (pos_x, pos_y))

        w = self.screen.get_width()
        h = rendered_text.get_height()
        onepercent_width = w / 100

        pos_x = 0
        pos_y = self.screen.get_height() - h

        current_width = onepercent_width * val

        if current_width > 0:
            surf = pygame.surface.Surface((current_width, h))

            surf.fill(LOADING_COLOR)
            self.screen.blit(surf, (pos_x, pos_y))


        # Pump event queue and flip display to keep the application alive
        pygame.event.pump()
        pygame.display.update()
