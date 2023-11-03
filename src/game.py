#!/usr/bin/env python
"""
    Game main class
    Initialized the base of the game
"""
import gettext
import os
import signal

import pygame
from pygame.locals import QUIT

import components.menu
import constants.game
import constants.headup
import utils.audio
from state.settingsstate import SettingsState
from utils.fps_counter import FPSCounter
from utils.screenshot import make_screenshot

_ = gettext.gettext

class Game:
    """ Main game class """

    def __init__(self):
        """ Constructor """
        pygame.mixer.pre_init(
            44100, 16, 2, 4096)  # For better and faster audio

        pygame.init()

        self.screen = None
        self.fps_counter = FPSCounter()
        self.running = True
        self.clock = pygame.time.Clock()
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.current_component = None
        self.settings_state = SettingsState(self.handle_settings_change)

    def start(self):
        """ Start game """

        # Load settings from file
        # IF no settings file exists create it
        if not self.settings_state.load():
            self.settings_state.save()
        self.settings_state.apply()

        self.init_screen()
        self.change_component(components.menu.Menu)

        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)
        self.main_loop()

    def handle_settings_change(self):
        self.settings_state.apply()

    def init_screen(self):
        """ Init the screen """
        flags = pygame.SCALED

        self.screen = None
        self.set_icon()
        pygame.display.set_caption(_('Grunzi'))

        if self.settings_state.fullscreen:
            flags = flags | pygame.FULLSCREEN

        if not self.screen:
            self.screen = pygame.display.set_mode(
                constants.game.SCREEN_SIZE,
                flags,
                vsync=int(self.settings_state.vsync))

    def set_icon(self):
        """ Set window icon """
        icon_path = os.path.join(self.data_dir, 'images', 'ui', 'icon.png')
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

    def toggle_fullscreen(self):
        """ Toggle fullscreen mode """
        self.settings_state.fullscreen = not self.settings_state.fullscreen
        self.settings_state.apply_and_save()

    def main_loop(self):
        """ Pygame MainLoop """
        while self.running:
            self.handle_events()
            self.update_screen()

    def handle_events(self):
        """ Handle events """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    self.screenshot()
                if event.mod & pygame.KMOD_ALT and event.key in [
                    pygame.K_RETURN, pygame.K_KP_ENTER
                ]:
                    self.toggle_fullscreen()

            self.current_component.handle_event(event)

    def quit(self, sig=None, frame=None):
        """ Quit game """
        self.running = False

    def screenshot(self):
        """ Save a screenshot  """
        make_screenshot(self.screen)
        camera_sound = os.path.join(self.data_dir, 'sounds', 'screenshot.ogg')
        utils.audio.play_sound(camera_sound)

    def update_screen(self):
        """ Update the screen  """
        # Filling the window with black color
        self.screen.fill((0, 0, 0))

        self.clock.tick(self.settings_state.limit_fps)

        self.current_component.update_screen(self.screen)

        if self.settings_state.show_fps:
            self.show_fps()

        pygame.display.flip()

    def show_fps(self):
        """ Show fps """
        self.fps_counter.get_fps(self.clock)
        self.current_component.render_text(self.fps_counter.get_fps_text(),
                                           (0, 247, 0),
                                           constants.headup.FPS_TEXT_POSITION)

    def change_component(self, component):
        """ Change component """
        if not component:
            component = components.menu.Menu

        if self.current_component:
            self.current_component.unmount()

        self.current_component = component(self.data_dir,
                                           self.change_component,
                                           self.settings_state)

        if self.current_component:
            self.current_component.set_screen(self.screen)

        self.current_component.mount()

        return self.current_component


game = Game()
game.start()
