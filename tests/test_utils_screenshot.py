import os
import unittest

import pygame

from utils.screenshot import make_screenshot


class ScreenshotTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

    def tearDown(self):
        pygame.quit()

    def test_make_screenshot(self):
        screenshot = make_screenshot(self.screen)
        self.assertTrue(os.path.exists(screenshot))
