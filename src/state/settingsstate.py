import pygame
import json
import os

from utils.path import get_userdata_path

SETTINGS_DEFAULT_FULLSCREEN = False
SETTINGS_DEFAULT_VOLUME = 0.8
SETTINGS_DEFAULT_SHOW_FPS = False
SETTINGS_DEFAULT_VSYNC = True
SETTINGS_DEFAULT_LIMIT_FPS = 0 # Default is unlimited

class SettingsState:
    def __init__(self, handle_settings_change):
        self.fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.old_fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.vsync = SETTINGS_DEFAULT_VSYNC
        self.show_fps = SETTINGS_DEFAULT_SHOW_FPS
        self.limit_fps = SETTINGS_DEFAULT_LIMIT_FPS

        self.music_volume = SETTINGS_DEFAULT_VOLUME

        self.handle_settings_change = handle_settings_change

    def reset_defaults(self):
        self.fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.old_fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.vsync = SETTINGS_DEFAULT_VSYNC
        self.show_fps = SETTINGS_DEFAULT_SHOW_FPS
        self.limit_fps = SETTINGS_DEFAULT_LIMIT_FPS
        
        self.music_volume = SETTINGS_DEFAULT_VOLUME

    def apply(self):
        # Fullscreen mode
        if self.fullscreen != self.old_fullscreen:
            pygame.display.toggle_fullscreen()
            self.old_fullscreen = self.fullscreen

        # Music volume
        pygame.mixer.music.set_volume(self.music_volume)

    def apply_and_save(self):
        self.apply()
        self.save()

    def get_settings_path(self):
        return os.path.join(get_userdata_path(), 'settings.json')

    def from_json(self, jsons):
        return json.loads(jsons)

    def load(self):
        if not os.path.exists(self.get_settings_path()):
            return False

        with open(self.get_settings_path(), 'r') as f:
            jsons = f.read()
            jsond = self.from_json(jsons)
            self.from_dict(jsond)

        return True

    def save(self):
        if not os.path.exists(get_userdata_path()):
            os.makedirs(get_userdata_path())

        with open(self.get_settings_path(), 'w') as f:
            f.write(self.to_json())

    def to_dict(self):
        return {
            'fullscreen': self.fullscreen,
            'show_fps': self.show_fps,
            'music_volume': self.music_volume,
            'vsync': self.vsync,
            'limit_fps': self.limit_fps
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def from_dict(self, settings):
        if 'fullscreen' in settings:
            self.fullscreen = settings['fullscreen']
            self.old_fullscreen = settings['fullscreen']

        if 'show_fps' in settings:
            self.show_fps = settings['show_fps']

        if 'music_volume' in settings:
            self.music_volume = settings['music_volume']

        if 'vsync' in settings:
            self.vsync = settings['vsync']

        if 'limit_fps' in settings:
            self.limit_fps = settings['limit_fps']

