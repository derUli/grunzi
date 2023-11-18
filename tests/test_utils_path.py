import unittest

from utils.path import is_windows, get_userdata_path


class PathTest(unittest.TestCase):
    def test_is_windows(self):
        self.assertEqual(bool(is_windows()), is_windows())

    def test_get_userdata_path(self):
        self.assertIn('grunzi', get_userdata_path().lower())
