import os
import unittest

from utils.path import is_windows
from utils.screen import supported_screen_resolutions
from utils.video import load_video, video_supported


class ScreenTest(unittest.TestCase):

    def test_screen_resolutions(self):
        self.assertIn('800x600', supported_screen_resolutions())