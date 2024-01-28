import gettext
import os
import unittest

import pygame
import utils.quality
from components.settings.controls import SettingsControls
from constants.quality import QUALITY_HIGH
from state.settingsstate import SettingsState

gettext.install('messages')


class ControlsText(unittest.TestCase):

    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1280, 720))

        utils.quality.settings_state = SettingsState()

        self.component = SettingsControls(
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

    def test_keyboard_controls(self):
        self.assertTrue(('Walk', 'Arrow_Keys.png') in self.component.keyboard_controls())

    def test_controller_controls(self):
        self.assertTrue(('Walk', '360_Dpad.png') in self.component.controller_controls())