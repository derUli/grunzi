""" Used to store launcher settings """
import logging
import os

import jsonpickle

from utils.path import get_settings_path

SETTINGS_STATE_VERSION = 2

class SettingsState:
    def __init__(self):
        # Screen resolution
        self.screen_resolution = [1280, 720]

        # Is fullscreen mode
        self.fullscreen = True

        # Vertical synchronisation
        self.vsync = True

        # Is sound disabled
        self.silent = False

        self.show_fps = False

        self.version = SETTINGS_STATE_VERSION

    @staticmethod
    def exists() -> bool:
        """
        Check if there is an existing settings file for the launcher
        @return: bool
        """
        return os.path.exists(get_settings_path())

    @staticmethod
    def load():
        try:
            return SettingsState._load()
        except ValueError as e:
            logging.error(e)
        except OSError as e:
            logging.error(e)
        except AttributeError as e:
            logging.error(e)

        return SettingsState()

    @staticmethod
    def _load():
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
