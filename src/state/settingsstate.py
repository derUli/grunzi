import json
import logging
import os

import pygame

import utils.audio
import utils.quality
from constants.quality import QUALITY_MEDIUM
from utils.path import get_userdata_path

SETTINGS_DEFAULT_FULLSCREEN = True
SETTINGS_DEFAULT_VSYNC = True
SETTINGS_DEFAULT_SCREEN_RESOLUTION = (1280, 720)
SETTINGS_DEFAULT_LIMIT_FPS = 0  # Default is unlimited
SETTINGS_DEFAULT_BLOOD = QUALITY_MEDIUM
SETTINGS_DEFAULT_SNOW = QUALITY_MEDIUM
SETTINGS_DEFAULT_BLOOM = False
SETTINGS_DEFAULT_FOG = True
SETTINGS_DEFAULT_SMOOTHSCALE = True
SETTINGS_DEFAULT_VOLUME = 1.0


class SettingsState:
    def __init__(self):
        """ Constructor """

        # Screen settings
        self.screen_resolution = SETTINGS_DEFAULT_SCREEN_RESOLUTION
        self.fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.old_fullscreen = SETTINGS_DEFAULT_FULLSCREEN
        self.vsync = SETTINGS_DEFAULT_VSYNC
        self.limit_fps = SETTINGS_DEFAULT_LIMIT_FPS

        # Audio settings
        self.sound_volume = SETTINGS_DEFAULT_VOLUME
        self.music_volume = SETTINGS_DEFAULT_VOLUME

        # Graphics settings
        self.blood = SETTINGS_DEFAULT_BLOOD
        self.bloom = SETTINGS_DEFAULT_BLOOM
        self.fog = SETTINGS_DEFAULT_FOG
        self.smoothscale = SETTINGS_DEFAULT_SMOOTHSCALE
        self.snow = SETTINGS_DEFAULT_SNOW

        # Needs restart
        self.needs_restart = False

    def apply_and_save(self):
        """ Apply and save """
        self.apply()
        self.save()

    def save(self):
        """ Save settings """

        logging.info('Save settings')
        if not os.path.exists(get_userdata_path()):
            os.makedirs(get_userdata_path())

        with open(self.get_settings_path(), 'w') as f:
            f.write(self.to_json())

    def apply(self):
        """ Apply settings """
        logging.info('Apply settings')
        logging.debug(self.to_json())

        """ Apply changes """
        # Fullscreen mode
        if self.fullscreen != self.old_fullscreen:
            logging.debug('Display mode changed ' + str(self.fullscreen))
            pygame.display.toggle_fullscreen()
            self.old_fullscreen = self.fullscreen

        # Music volume
        pygame.mixer.music.set_volume(self.music_volume)
        utils.audio.SOUND_VOLUME = self.sound_volume

        utils.quality.settings_state = self

    def get_settings_path(self):
        """ Get settings file path """
        return os.path.join(get_userdata_path(), 'settings.json')

    def from_json(self, jsons):
        """ Load from json """
        return json.loads(jsons)

    def load(self):
        """ Load from file """
        if not os.path.exists(self.get_settings_path()):
            return False

        with open(self.get_settings_path(), 'r') as f:
            jsons = f.read()
            jsond = self.from_json(jsons)
            self.from_dict(jsond)

        return True

    def to_dict(self):
        """ To dict """
        return {
            'fullscreen': self.fullscreen,
            'sound_volume': self.sound_volume,
            'music_volume': self.music_volume,
            'vsync': self.vsync,
            'limit_fps': self.limit_fps,
            'screen_resolution': self.screen_resolution,
            'blood': self.blood,
            'bloom': self.bloom,
            'fog': self.fog,
            'snow': self.snow,
            'smoothscale': self.smoothscale,
            
        }

    def to_json(self):
        """ To JSON """
        return json.dumps(self.to_dict())

    def from_dict(self, settings):
        """ From dictionary """

        if 'fullscreen' in settings:
            self.fullscreen = bool(settings['fullscreen'])
            self.old_fullscreen = bool(settings['fullscreen'])

        if 'sound_volume' in settings:
            self.sound_volume = float(settings['sound_volume'])

        if 'music_volume' in settings:
            self.music_volume = float(settings['music_volume'])

        if 'vsync' in settings:
            self.vsync = bool(settings['vsync'])

        if 'limit_fps' in settings:
            self.limit_fps = int(settings['limit_fps'])

        if 'screen_resolution' in settings:
            self.screen_resolution = tuple(settings['screen_resolution'])

        if 'blood' in settings:
            self.blood = int(settings['blood'])

        if 'bloom' in settings:
            self.bloom = bool(settings['bloom'])

        if 'fog' in settings:
            self.fog = bool(settings['fog'])

        if 'snow' in settings:
            self.snow = int(settings['snow'])

        if 'smoothscale' in settings:
            self.smoothscale = bool(settings['smoothscale'])
