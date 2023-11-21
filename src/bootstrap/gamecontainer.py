#!/usr/bin/env python
"""
    Game main class
    Initialized the base of the game
"""
import logging
import os
import platform
import signal

import pygame
from pygame.locals import QUIT

import components.menu
from utils.audio import play_sound, get_devices
from state.settingsstate import SettingsState
from utils import xbox_360_controller
from utils.helper import get_version
from utils.screenshot import make_screenshot
from utils.string import label_value

from GPUtil.GPUtil import getGPUs

class GameContainer:
    """ Main game class """

    def __init__(self, root_dir, enable_edit_mode=False, disable_controller=False, disable_ai=False,
                 enable_mouse=False):
        """ Constructor """
        self.root_dir = root_dir
        self.data_dir = os.path.join(root_dir, 'data')
        self.screen = None
        self.running = True
        self.clock = pygame.time.Clock()
        self.current_component = None
        self.settings_state = SettingsState(self.handle_settings_change)
        self.enable_edit_mode = enable_edit_mode
        self.gamepad = None
        self.disable_controller = disable_controller
        self.disable_ai = disable_ai
        self.enable_mouse = enable_mouse
        self.__main__ = None

    def start(self, component=components.menu.Menu):
        """ Start game """
        version_file = os.path.join(self.root_dir, 'LICENSE')

        logging.info(label_value('OS', platform.platform()))
        logging.info(label_value('CPU', platform.processor()))

        if callable(getGPUs):
            gpus = getGPUs()
            for gpu in gpus:
                logging.info(label_value('GPU', gpu.name))
        else:
            logging.info(label_value('GPU', 'Unknown'))

        logging.info(label_value('Python version', platform.python_version()))
        logging.info(label_value('Pygame version', pygame.version.ver))
        logging.info(label_value('SDL Version', pygame.version.SDL))
        logging.info(label_value('Grunzi Version', get_version(version_file)))

        pygame.mixer.pre_init(
            44100, 16, 2, 4096)  # For better and faster audio

        pygame.init()

        audio_devices = get_devices()

        for device in audio_devices:
            logging.info(label_value('Audio device', device))

        # Load settings from file
        # IF no settings file exists create it
        if not self.settings_state.load():
            self.settings_state.save()

        self.settings_state.apply()

        self.init_screen()
        if not self.disable_controller:
            self.init_controller()

        self.change_component(component)

        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)

        self.mainloop()

    def handle_settings_change(self):
        self.settings_state.apply()

    def init_screen(self):
        """ Init the screen """
        flags = pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF

        self.screen = None
        logging.info('Init screen')
        logging.info(label_value('Screen resolution', str(self.settings_state.screen_resolution)))
        pygame.display.set_caption(_('Grunzi'))

        if self.settings_state.fullscreen:
            flags = flags | pygame.FULLSCREEN

        if not self.screen:
            self.screen = pygame.display.set_mode(
                self.settings_state.screen_resolution,
                flags,
                vsync=int(self.settings_state.vsync))

        self.set_icon()

    def init_controller(self):
        """ Init Controller """
        try:
            self.gamepad = xbox_360_controller.Controller()
            logging.info(label_value('Controller', self.gamepad.joystick.get_name()))
            return True
        except pygame.error:
            logging.info('No controller found')
            return False

    def set_icon(self):
        """ Set window icon """
        icon_path = os.path.join(self.data_dir, 'images', 'ui', 'icon.png')
        icon = pygame.image.load(icon_path)
        pygame.display.set_icon(icon)

    def toggle_fullscreen(self):
        """ Toggle fullscreen mode """
        self.settings_state.fullscreen = not self.settings_state.fullscreen
        self.settings_state.apply_and_save()
        self.set_icon()

    def mainloop(self):
        """ Pygame MainLoop """
        while self.running:
            try:
                self.handle_events()
            except SystemError as e:
                logging.error(e)

            self.draw()
            self.ai()

    def handle_events(self):

        """ Handle events """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
                return
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
        self.current_component.do_quit = True
        self.running = False

    def screenshot(self):
        """ Save a screenshot  """
        make_screenshot(self.screen)
        camera_sound = os.path.join(self.data_dir, 'sounds', 'common', 'screenshot.ogg')
        play_sound(camera_sound)

    def draw(self):
        """ Update the screen  """
        # Filling the window with black color

        self.current_component.draw(self.screen)

        self.tick()
        pygame.display.update()

    def ai(self):
        if self.current_component:
            self.current_component.ai()

    def tick(self):
        self.clock.tick(self.settings_state.limit_fps)

    def change_component(self, component):
        """ Change component """
        if not component:
            component = components.menu.Menu

        if self.current_component:
            self.current_component.unmount()

        if callable(component):
            self.current_component = component(
                self.data_dir,
                self.change_component,
                self.settings_state,
                enable_edit_mode=self.enable_edit_mode,
                gamepad=self.gamepad
            )

        else:
            self.current_component = component

        if not self.current_component:
            return

        self.current_component.__main__ = self.__main__

        self.current_component.image_cache.clear()
        self.current_component.set_screen(self.screen)
        self.current_component.disable_ai = self.disable_ai
        self.current_component.enable_mouse = self.enable_mouse
        self.current_component.mount()

        return self.current_component
