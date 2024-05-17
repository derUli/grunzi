""" Used to store launcher settings """

import logging
import os

import jsonpickle

from constants.audio import DEFAULT_AUDIO_BACKEND
from utils.audio import normalize_volume
from utils.path import get_settings_path

SETTINGS_STATE_VERSION = 9


class SettingsState:
    def __init__(self):
        # Video
        self.screen_resolution = [1280, 720]
        self.fullscreen = True
        self.borderless = False
        self.vsync = True
        self.show_fps = False
        self.sky = True
        self.shaders = True
        self.traffic = True
        self.videos = True

        self.antialiasing = 4

        # Audio
        self.audio_backend = DEFAULT_AUDIO_BACKEND
        self._music_volume = 1
        self._sound_volume = 1
        self._muted = False
        self.first_start = False

        # SettingState
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
        """
        Loads the settings state
        @return: bool
        """
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

            if SettingsState().version != state.version:
                return SettingsState()

            return state

    def save(self) -> None:
        """ Save settings as json file """
        with open(get_settings_path(), 'w') as f:
            f.write(jsonpickle.encode(self, unpicklable=True))

    @property
    def music_volume(self):
        if self.is_silent() or self._muted:
            return 0.0

        return self._music_volume

    @music_volume.setter
    def music_volume(self, volume):
        volume = normalize_volume(volume)

        self._music_volume = volume

    @property
    def sound_volume(self):
        if self.is_silent() or self._muted:
            return 0.0

        return self._sound_volume

    @sound_volume.setter
    def sound_volume(self, volume):
        if volume < 0:
            volume = 0.0

        if volume > 1:
            volume = 1.0

        volume = round(volume, 2)
        logging.info('Audio: New volume %s', volume)
        self._sound_volume = volume

    def mute(self):
        self._muted = True

    def unmute(self):
        self._muted = False

    def is_silent(self):
        return self.audio_backend == 'silent'
