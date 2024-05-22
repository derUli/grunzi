import os
import unittest

from constants.audio import audio_backends, DEFAULT_AUDIO_BACKEND
from state.settingsstate import SettingsState
from state.viewstate import ViewState
from utils.audio import normalize_volume, streaming_enabled, MusicQueue
from utils.path import is_windows


class ConstantsAudioTest(unittest.TestCase):
    def test_audio_backends(self):
        self.assertIn('auto', audio_backends())
        self.assertIn('silent', audio_backends())

    def test_default(self):
        self.assertEqual('auto', DEFAULT_AUDIO_BACKEND)