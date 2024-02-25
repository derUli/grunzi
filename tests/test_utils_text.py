import unittest

from utils.text import label_value


class TextTest(unittest.TestCase):
    def test_label_value(self):
        self.assertEqual('Value: 123.0', label_value('Value', 123.0))
