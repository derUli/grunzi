import unittest

from utils.audio import normalize_volume, streaming_enabled
from utils.path import is_windows


class AudioTest(unittest.TestCase):
    def test_normalize_volume(self):
        self.assertEqual(1.0, normalize_volume(19.95))
        self.assertEqual(0.0, normalize_volume(-123))
        self.assertEqual(0.46, normalize_volume(0.456789))

    def test_streaming_enabled(self):
        self.assertEqual(streaming_enabled(), is_windows())
