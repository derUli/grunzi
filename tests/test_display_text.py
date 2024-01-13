import pygame
import os
import unittest
from utils.display_text import DisplayText

class DisplayTextTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1280, 720))
        self.display_text = DisplayText(os.path.dirname(__file__))


    def tearDown(self):
        pygame.quit()

    def test_is_visible_false(self):
        self.assertFalse(self.display_text.is_visible())