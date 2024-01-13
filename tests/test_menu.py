import unittest

import pygame
from pygame_menu import Menu

from utils.menu import make_menu, get_longest_option


class MenuTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.display.set_mode((1280, 720))

    def tearDown(self):
        pygame.quit()

    def test_make_menu(self):
        self.assertIsInstance(make_menu('Foobar', 30), Menu)

    def test_get_longest_option(self):
        options = [
            ('Foobar', 1),
            ('foo', 2),
            ('Piggy', 3)
        ]

        self.assertEqual('Foobar', get_longest_option(options))
