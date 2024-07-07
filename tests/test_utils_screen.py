import unittest

from utils.screen import supported_screen_resolutions


class ScreenTest(unittest.TestCase):

    def test_screen_resolutions(self):
        self.assertIn('1024x768', supported_screen_resolutions())
