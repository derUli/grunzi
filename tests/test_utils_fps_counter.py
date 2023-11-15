import unittest

from utils.string import natural_keys
class StringTest(unittest.TestCase):
    def test_direction(self):
        arr = [
            '1',
            '001',
            '01',
            '00'
        ]

        self.assertEqual(['00', '001', '01', '1'], sorted(arr))
        self.assertEqual(['00', '1', '001', '01'], sorted(arr, key=natural_keys))