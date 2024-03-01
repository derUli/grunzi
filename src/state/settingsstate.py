import os

import jsonpickle

from utils.path import get_settings_path


class SettingsState:
    def __init__(self):
        # Is fullscreen mode
        self.fullscreen = False
        # Screen resolution
        self.screen_resolution = [1280, 720]

        # Is sound disabled
        self.silent = False

        # Is debug
        self.debug = False
        # Is controller enabled
        self.controller = False

    @staticmethod
    def exists():
        return os.path.exists(get_settings_path())

    @staticmethod
    def load():
        with open(get_settings_path(), 'r') as f:
            return jsonpickle.decode(f.read())

    def save(self):
        with open(get_settings_path(), 'w') as f:
            f.write(jsonpickle.encode(self, unpicklable=True))
