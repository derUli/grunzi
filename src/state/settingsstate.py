""" Used to store game settings """

import logging
import os

import jsonpickle

from constants.audio import DEFAULT_AUDIO_BACKEND
from constants.settings import DEFAULT_VSYNC, DEFAULT_FULLSCREEN, DEFAULT_BORDERLESS, DEFAULT_SHOW_FPS, \
    DEFAULT_FILMGRAIN, DEFAULT_FOG, DEFAULT_COLOR_TINT, DEFAULT_QUALITY, DEFAULT_MUSIC_VOLUME, DEFAULT_SOUND_VOLUME, \
    DEFAULT_ATMO_VOLUME, DEFAULT_MUTED, DEFAULT_FIRST_START, DEFAULT_VIBRATION, DEFAULT_ANTIALIASING, QualityPreset
from utils.media.audio import normalize_volume
from utils.path import get_settings_path

SETTINGS_STATE_VERSION = 19


class SettingsState:
    """ Game settings """

    def __init__(self):
        """ Constructor """

        # Video
        self.screen_resolution = [1280, 720]
        self.fullscreen = DEFAULT_FULLSCREEN
        self.borderless = DEFAULT_BORDERLESS
        self.vsync = DEFAULT_VSYNC
        self.show_fps = DEFAULT_SHOW_FPS

        self._antialiasing = DEFAULT_ANTIALIASING
        self._filmgrain = DEFAULT_FILMGRAIN
        self._fog = DEFAULT_FOG
        self._color_tint = DEFAULT_COLOR_TINT

        self._quality = DEFAULT_QUALITY

        # Audio
        self.audio_backend = DEFAULT_AUDIO_BACKEND
        self._music_volume = DEFAULT_MUSIC_VOLUME
        self._sound_volume = DEFAULT_SOUND_VOLUME
        self._atmo_volume = DEFAULT_ATMO_VOLUME
        self._muted = DEFAULT_MUTED

        # Controllers
        self.vibration = DEFAULT_VIBRATION

        # Other
        self.version = SETTINGS_STATE_VERSION
        self.first_start = DEFAULT_FIRST_START

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

        @return: SettingsState
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
        """
        Actually loads the settings state

        @return: SettingsState
        """
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

        logging.info('Music: New volume %s', volume)
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

    @property
    def atmo_volume(self):
        if self.is_silent() or self._muted:
            return 0.0

        return self._atmo_volume

    @atmo_volume.setter
    def atmo_volume(self, volume):
        if volume < 0:
            volume = 0.0

        if volume > 1:
            volume = 1.0

        volume = round(volume, 2)
        logging.info('Atmo: New volume %s', volume)
        self._atmo_volume = volume

    @property
    def filmgrain(self):
        return self._filmgrain

    @filmgrain.setter
    def filmgrain(self, intensity: float):
        self._filmgrain = intensity

    @property
    def fog(self):
        return self._fog

    @fog.setter
    def fog(self, val):
        self._fog = val

    @property
    def color_tint(self):
        return self._color_tint

    @color_tint.setter
    def color_tint(self, val):
        self._color_tint = val

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self, quality):
        self._quality = int(quality)
        preset = QualityPreset(self.quality)

        self._filmgrain = preset.filmgrain
        self.fog = preset.fog
        self.color_tint = preset.color_tint
        self.antialiasing = preset.antialiasing

    @property
    def antialiasing(self):
        return self._antialiasing

    @antialiasing.setter
    def antialiasing(self, val):
        val = int(round(val))

        if val > 1 and val < 2:
            val = 2

        if val > 3 and val < 4:
            val = 4

        if val > 4 and val < 8:
            val = 8

        if val > 8:
            val = 16

        self._antialiasing = val

    def mute(self) -> None:
        """ Mute sound """
        self._muted = True

    def unmute(self) -> None:
        """ Unmute sound """
        self._muted = False

    def is_silent(self):
        return self.audio_backend == 'silent'
