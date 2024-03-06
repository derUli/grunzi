""" Used to store launcher settings """
import os

import jsonpickle

from utils.path import get_settings_path


class SettingsState:
    def __init__(self):
        # Screen resolution
        self.screen_resolution = [1280, 720]

        # Is fullscreen mode
        self.fullscreen = False

        # Vertical synchronisation
        self.vsync = True

        # Is sound disabled
        self.silent = False

        # Is controller enabled
        self.controller = False

        self.version = 2

    @staticmethod
    def exists() -> bool:
        """
        Check if there is an existing settings file for the launcher
        @return: bool
        """
        return os.path.exists(get_settings_path())

    @staticmethod
    def load():
        with open(get_settings_path(), 'r') as f:
            state = jsonpickle.decode(f.read())

            # jsonpickle don't calls __init__()
            # So when loading a state attributes added since then are missing
            # I added a version number
            # If the state version from the code is newer than the stored version
            # discard the old settings state and return a new one

            if SettingsState().version > state.version:
                return SettingsState()

            return state

    def save(self) -> None:
        """ Save settings as json file """
        with open(get_settings_path(), 'w') as f:
            f.write(jsonpickle.encode(self, unpicklable=True))
