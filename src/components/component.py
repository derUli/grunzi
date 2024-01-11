import os

import pygame

import constants.game
import constants.headup
import utils.audio
import utils.image
import utils.quality
from constants.headup import UI_MARGIN
from utils.animation import Animation


class Component(object):

    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        self.data_dir = data_dir
        self.handle_change_component = handle_change_component
        self.image_cache = utils.image.ImageCache()
        self.settings_state = settings_state
        self.enable_edit_mode = enable_edit_mode
        self.gamepad = gamepad
        self.do_quit = False
        self.__main__ = None
        self.pressed_keys = []

        self.monotype_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', constants.game.MONOTYPE_FONT),
            constants.game.DEBUG_OUTPUT_FONT_SIZE)

        animation_dir = os.path.join(
            data_dir,
            'images',
            'sprites',
            'animations',
            'film_grain')

        self.film_grain = Animation(
            animation_dir,
            refresh_interval=0.13,
            start_frame=0,
            size=self.settings_state.screen_resolution
        )

    # Create Text
    def render_text(self, what, color, where):
        """ Render a text """
        text = self.monotype_font.render(
            what,
            utils.quality.font_antialiasing_enabled(),
            pygame.Color(color)
        )

        self.screen.blit(text, where)

    def draw_notification(self, what, color, screen):
        """ Draw notification text in the bottom right of the screen"""
        text = self.monotype_font.render(
            what,
            utils.quality.font_antialiasing_enabled(),
            pygame.Color(color)
        )

        w, h = text.get_size()

        x, y = screen.get_size()

        x -= w
        y -= h

        y -= UI_MARGIN
        x -= UI_MARGIN

        where = (x, y)

        self.render_text(what, color, where)

    def draw(self, screen):
        """ Fill screen with black """
        screen.fill((0, 0, 0))

    def handle_event(self, event):
        """ Handle an event """
        return

    def set_screen(self, screen):
        """ Set screen """
        self.screen = screen

    def mount(self):
        return

    def ai(self):
        return

    def play_music(self, file, repeat=-1):
        file = os.path.join(self.data_dir, 'music', file)
        utils.audio.play_music(file, repeat)

    def unmount(self):
        return True

    def draw_film_grain(self, screen):
        """ Draw film grain """
        if not utils.quality.film_grain():
            return

        grain = self.film_grain.get_frame()
        grain.set_alpha(80)
        screen.blit(grain, (0, 0))
