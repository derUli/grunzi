import os
import time
import unittest

from state.settingsstate import SettingsState
from state.viewstate import ViewState
from utils.fpscounter import FPSCounter
from utils.media.audio import normalize_volume, streaming_enabled, MusicQueue
from utils.path import is_windows


class FpsCounterTest(unittest.TestCase):
    def test_reset(self):
        counter = FPSCounter()
        counter.current_fps = 60
        self.assertEqual(counter.current_fps, 60)

        counter.reset()
        self.assertNotEqual(counter.current_fps, 60)

    def test_update(self):
        counter = FPSCounter()
        counter.update(144)

        self.assertNotEqual(counter.current_fps, 144)

        time.sleep(1)

        counter.update(144)
        self.assertEqual(counter.current_fps, 144)