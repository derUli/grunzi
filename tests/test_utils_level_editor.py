import os
import unittest

import pygame

from sprites.sprite import Sprite
from utils.image import ImageCache
from utils.level_editor import get_editor_blocks


class LevelEditorTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1280, 720))

    def tearDown(self):
        pygame.quit()

    def test_get_level_editor(self):
        sprites_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'sprites')
        cache = ImageCache()
        blocks = get_editor_blocks(sprites_dir, cache)

        for block in blocks:
            self.assertTrue(Sprite, block)

