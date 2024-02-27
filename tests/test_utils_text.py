import unittest

from utils.text import label_value, get_style


class TextTest(unittest.TestCase):
    def test_label_value(self):
        self.assertEqual('Value: 123.0', label_value('Value', 123.0))

    def test_get_style(self):
        self.assertIn('font_name', get_style())