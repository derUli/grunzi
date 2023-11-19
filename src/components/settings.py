import logging
import os
import subprocess
import sys

from components.component import Component
from components.controls import Controls
from components.settings_audio import SettingsAudio
from components.settings_video import SettingsVideo
from constants.headup import PIGGY_PINK
from constants.quality import QUALITY_LOW
from utils.animation import Animation
from utils.helper import get_version
from utils.menu import make_menu


class Settings(Component):
    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)

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

        self.needs_restart = False
        self.menu = None

        version_file = os.path.join(self.data_dir, '..', 'VERSION')
        self.version_number = get_version(version_file)

    def draw(self, screen):
        self.draw_menu(screen)

    def handle_back(self):
        if self.needs_restart:
            self.restart_app()
            return
        component = self.handle_change_component(None)
        component.video = self.video
        self.menu.disable()

    def restart_app(self):
        logging.debug('Restart application to apply settings')

        command = [sys.executable] + sys.argv

        # If we are running from Exe
        if getattr(sys, "frozen", False):
            command = sys.argv

        subprocess.Popen(command)
        sys.exit()

    def handle_video(self):
        component = self.handle_change_component(SettingsVideo)
        component.video = self.video
        component.old_component = self
        self.menu.disable()

    def handle_audio(self):
        component = self.handle_change_component(SettingsAudio)
        component.video = self.video
        component.old_component = self
        self.menu.disable()

    def handle_controls(self):
        """ Handle open settings menu  """
        component = self.handle_change_component(Controls)
        component.old_component = self

        self.menu.disable()

    def draw_background(self):
        if self.settings_state.quality >= QUALITY_LOW:
            video_frame = self.video.get_frame()
            if video_frame:
                self.screen.blit(video_frame, (0, 0))

        self.draw_notification(self.version_number, PIGGY_PINK, self.screen)

    def draw_menu(self, screen):
        menu = make_menu(_('Settings'), self.settings_state.limit_fps)

        menu.add.button(_('Video'), self.handle_video)
        menu.add.button(_('Audio'), self.handle_audio)
        menu.add.button(_('Controls'), self.handle_controls)
        menu.add.button(_('Back To Main Menu'), self.handle_back)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
