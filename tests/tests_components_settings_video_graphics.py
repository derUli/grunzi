import gettext
import os
import unittest

import pygame

import utils.quality
from components.settings.video.graphics import SettingsGraphics
from constants.quality import QUALITY_HIGH
from state.settingsstate import SettingsState

gettext.install('messages')


class VideoGraphicsTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1280, 720))

        utils.quality.settings_state = SettingsState()

        self.component = SettingsGraphics(
            os.path.join('..', 'src', 'data'),
            self.dummy,
            SettingsState()
        )

    def tearDown(self):
        pygame.quit()
        self.component = None

        utils.quality.settings_state = None

    def dummy(self, component):
        return

    def test_get_blood_items(self):
        self.assertTrue(('High', QUALITY_HIGH) in self.component.get_blood_items())

    def test_get_fire_items(self):
        self.assertTrue(('High', QUALITY_HIGH) in self.component.get_fire_items())

    def test_get_weather_items(self):
        self.assertTrue(('High', QUALITY_HIGH) in self.component.get_weather_items())
