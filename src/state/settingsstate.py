import os

from utils.path import get_settings_path
import jsonpickle


class SettingsState:
    def __init__(self):
        self.fullscreen = False
        self.screen_resolution = [1280, 720]
        self.silent = False

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