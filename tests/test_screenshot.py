import os
import unittest

import pygame

from utils.screenshot import make_screenshot, SCREENSHOT_DIR, DUMP_DIR


class ScreenshotTest(unittest.TestCase):
    def test_make_screenshot_screenshot(self):
        surface = pygame.surface.Surface((100, 100))
        surface.fill((255, 255, 255))
        output_file = make_screenshot(surface)
        self.assertIn(SCREENSHOT_DIR, output_file)
        self.assertNotIn('dumps', output_file)
        self.assertTrue(os.path.exists(output_file))

    def test_make_screenshot_dumps(self):
        surface = pygame.surface.Surface((100, 100))
        surface.fill((255, 255, 255))
        output_file = make_screenshot(surface, DUMP_DIR)
        self.assertNotIn('screenshots', output_file)
        self.assertIn('dumps', output_file)
        self.assertTrue(os.path.exists(output_file))
