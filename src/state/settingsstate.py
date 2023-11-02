import pygame

SETTINGS_DEFAULT_FULLSCREEN = False
SETTINGS_DEFAULT_VOLUME = 1.0

class SettingsState:
    def __init__(self, handle_settings_change):
        self.show_fps = True
        self.fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.old_fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.music_volume = SETTINGS_DEFAULT_VOLUME
        self.handle_settings_change = handle_settings_change

    def reset_defaults(self):
        self.fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.show_fps = True
        self.music_volume = SETTINGS_DEFAULT_VOLUME

    def apply(self):
        # Fullscreen mode
        if self.fullscreen != self.old_fullscreen:
            pygame.display.toggle_fullscreen()
            self.old_fullscreen = self.fullscreen
        
        # Music volume
        pygame.mixer.music.set_volume(self.music_volume)