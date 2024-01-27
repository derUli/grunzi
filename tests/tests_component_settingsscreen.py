import os
import unittest

import pygame

import utils.quality
from components.settings.video.screen import  SettingsScreen
from state.settingsstate import SettingsState


class VideoScreenTest(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1280, 720))

        utils.quality.settings_state = SettingsState()

        self.component = SettingsScreen(
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

    def test_get_screen_resolution_items(self):
        self.assertTrue(('1280x720', (1280, 720)) in self.component.get_screen_resolution_items())