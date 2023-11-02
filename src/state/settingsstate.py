import pygame

class SettingsState:
    def __init__(self, handle_settings_change):
        self.show_fps = True
        self.fullscreen = False
        self.old_fullscreen = False
        self.handle_settings_change = handle_settings_change

    def reset_defaults(self):
        self.fullscreen = False
        self.show_fps = False
