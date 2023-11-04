import os

import pygame
import logging

import constants.game
import constants.headup
import utils.audio
import utils.image
import utils.xbox_360_controller as xbox360_controller

class Component(object):

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False):
        """ Constructor """
        self.data_dir = data_dir
        self.handle_change_component = handle_change_component
        self.image_cache = utils.image.ImageCache()
        self.settings_state = settings_state
        self.enable_edit_mode = enable_edit_mode
        self.controller = None

        try:
            self.controller = xbox360_controller.Controller()
        except pygame.error:
            logging.debug('No controller found')

        self.monotype_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', constants.game.MONOTYPE_FONT),
            constants.game.DEBUG_OUTPUT_FONT_SIZE)


    # Create Text
    def render_text(self, what, color, where):
        text = self.monotype_font.render(what, 1, pygame.Color(color))
        self.screen.blit(text, where)

    def update_screen(self, screen):
        screen.fill((0, 0, 0))

    def handle_event(self, event):
        return

    def set_screen(self, screen):
        self.screen = screen

    def mount(self):
        return

    def play_music(self, file, repeat=-1):
        file = os.path.join(self.data_dir, 'music', file)
        utils.audio.play_music(file, repeat)

    def unmount(self):
        return
