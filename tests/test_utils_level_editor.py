import os
import unittest

import pygame

import utils.quality
from sprites.sprite import Sprite
from state.settingsstate import SettingsState
from utils.image import ImageCache
from utils.level_editor import get_editor_blocks


class LevelEditorTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1280, 720))
        utils.quality.settings_state = SettingsState()

    def tearDown(self):
        pygame.quit()
        utils.quality.settings_state = None

    def test_get_level_editor(self):
        sprites_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'images', 'sprites')
        )
        cache = ImageCache()
        blocks = get_editor_blocks(sprites_dir, cache)

        for block in blocks:
            self.assertTrue(Sprite, block)
