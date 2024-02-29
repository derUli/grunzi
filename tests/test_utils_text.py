import unittest

import arcade

from utils.text import label_value, get_style, create_text
from window.gamewindow import GameWindow


class TextTest(unittest.TestCase):
    def setUp(self):
        GameWindow()
    def test_label_value(self):
        self.assertEqual('Value: 123.0', label_value('Value', 123.0))

    def test_get_style(self):
        self.assertIn('font_name', get_style())

    def test_create_test(self):
        text = create_text('foobar')

        self.assertIsInstance(text, arcade.text_pyglet.Text)