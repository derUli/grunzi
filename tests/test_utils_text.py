import os
import unittest

import arcade

from state.viewstate import ViewState
from utils.text import label_value, get_style, create_text
from window.gamewindow import GameWindow


class TextTest(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src'
        )
        state = ViewState(root_dir, map_name='world')
        state.preload()
        GameWindow()

    def tearDown(self):
        arcade.exit()

    def test_label_value(self):
        self.assertEqual('Value: 123.0', label_value('Value', 123.0))

    def test_get_style(self):
        self.assertEqual('Laila', get_style()['hover']['font_name'])

    def test_create_text(self):
        text = create_text('Foobar')

        self.assertIsInstance(text, arcade.text.Text)
