import os
import unittest

import arcade

from state.viewstate import ViewState
from utils.gui import get_button_style, get_slider_style
from utils.text import label_value, create_text
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

    def test_get_button_style(self):
        self.assertEqual('Laila', get_button_style()['hover']['font_name'])

    def test_get_slider_style(self):
        slider_style = get_slider_style()
        self.assertIsInstance(slider_style, dict)

        for val in slider_style.values():
            self.assertIsInstance(val, arcade.gui.UISlider.UIStyle)
    def test_create_text(self):
        
        text = create_text('Foobar')
        self.assertIsInstance(text, arcade.text.Text)
