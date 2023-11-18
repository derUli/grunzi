import unittest

from utils.string import natural_keys, label_value
class StringTest(unittest.TestCase):
    def test_natural_keys(self):
        arr = [
            '1',
            '001',
            '01',
            '00'
        ]

        self.assertEqual(['00', '001', '01', '1'], sorted(arr))
        self.assertEqual(['00', '1', '001', '01'], sorted(arr, key=natural_keys))

    def test_label_value(self):
        self.assertEqual(
            'Level: 123.45',
            label_value('Level', 123.45)
        )