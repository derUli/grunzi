import unittest

from utils.path import is_windows, get_userdata_path, get_settings_path, get_savegame_path


class PathTest(unittest.TestCase):
    def test_is_windows(self):
        self.assertTrue(bool == type(is_windows()))

    def test_get_userdata_path(self):
        self.assertTrue('grunzi' in get_userdata_path().lower())

    def test_get_settings_path(self):
        self.assertIn('settings.json', get_settings_path())

    def test_get_savegame_path(self):
        self.assertIn('savegames', get_savegame_path('foo'))
        self.assertIn('foo.json', get_savegame_path('foo'))
