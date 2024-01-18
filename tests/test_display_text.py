import os
import unittest
import pygame
import time
from utils.display_text import DisplayText


class DisplayTextTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        data_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src',
            'data'
        )
        self.display_text = DisplayText(data_dir)

    def tearDown(self):
        pygame.quit()

    def test_is_visible_false(self):
        self.display_text.draw(self.screen, (0, 0))
        self.assertFalse(self.display_text.is_visible())

    def test_is_visible_true(self):
        self.display_text.show_text('Hi')
        self.display_text.draw(self.screen, (0, 0))
        self.assertTrue(self.display_text.is_visible())



    def test_is_visible_wait(self):
        self.display_text.show_text('Hi')
        self.display_text.draw(self.screen, (0, 0))
        time.sleep(3)
        self.display_text.draw(self.screen, (0, 0))
        self.assertFalse(self.display_text.is_visible())