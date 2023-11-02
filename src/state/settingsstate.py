import pygame
import json

SETTINGS_DEFAULT_FULLSCREEN = False
SETTINGS_DEFAULT_VOLUME = 1.0
SETTINGS_SHOW_FPS_DEFAULT = True

class SettingsState:
    def __init__(self, handle_settings_change):
        self.fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.old_fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.show_fps = SETTINGS_SHOW_FPS_DEFAULT
        self.music_volume = SETTINGS_DEFAULT_VOLUME

        self.handle_settings_change = handle_settings_change

    def reset_defaults(self):
        self.fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.show_fps = SETTINGS_SHOW_FPS_DEFAULT
        self.music_volume = SETTINGS_DEFAULT_VOLUME

    def apply(self):
        # Fullscreen mode
        if self.fullscreen != self.old_fullscreen:
            pygame.display.toggle_fullscreen()
            self.old_fullscreen = self.fullscreen
        
        # Music volume
        pygame.mixer.music.set_volume(self.music_volume)


    def to_dict(self):
        return {
            'fullscreen': self.fullscreen,
            'show_fps': self.show_fps,
            'music_volume': self.music_volume
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def from_dict(self, settings):
        if 'fullscreen' in settings:
            self.fullscreen = settings.fullscreen
            self.old_fullscreen = settings.fullscreen

        if 'show_fps' in settings:
            self.show_fps = settings.show_fps
        
        if 'music_volume' in settings:
            self.music_volume = settings.volume