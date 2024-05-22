import unittest

from constants.audio import audio_backends, DEFAULT_AUDIO_BACKEND


class ConstantsAudioTest(unittest.TestCase):
    def test_audio_backends(self):
        self.assertIn('auto', audio_backends())
        self.assertIn('silent', audio_backends())

    def test_default(self):
        self.assertEqual('auto', DEFAULT_AUDIO_BACKEND)
