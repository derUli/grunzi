import os
import unittest

from state.settingsstate import SettingsState
from state.viewstate import ViewState
from utils.media.audio import normalize_volume, streaming_enabled, MusicQueue
from utils.path import is_windows


class AudioTest(unittest.TestCase):
    def setUp(self):
        root_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src'
        )

        settings = SettingsState()
        self.state = ViewState(root_dir, settings=settings)

    def test_normalize_volume(self):
        self.assertEqual(1.0, normalize_volume(19.95))
        self.assertEqual(0.0, normalize_volume(-123))
        self.assertEqual(0.46, normalize_volume(0.456789))

    def test_streaming_enabled(self):
        self.assertEqual(streaming_enabled(), is_windows())

    def test_set_files(self):
        queue = MusicQueue(self.state)
        queue.set_files(['foo', 'bar'])
        self.assertEqual(['foo', 'bar'], queue.files)

    def test_from_directory(self):
        queue = MusicQueue(self.state)
        queue.from_directory(
            os.path.join(self.state.sound_dir, 'atmos'))

        self.assertIn('beach.ogg', queue.files[0])

    def test_shuffle(self):
        queue = MusicQueue(self.state)
        queue.from_directory(
            os.path.join(self.state.sound_dir, 'pig'))
        files = queue.queue

        queue.shuffle()
        self.assertNotEqual(files, queue.queue)

    def test_play(self):
        queue = MusicQueue(self.state)
        queue.from_directory(
            os.path.join(self.state.sound_dir, 'pig'))

        queue.play()
        queue.update()

        self.assertTrue(queue.player.playing)

    def test_pause(self):
        queue = MusicQueue(self.state)
        queue.from_directory(
            os.path.join(self.state.sound_dir, 'pig'))

        queue.play()
        queue.pause()
        self.assertFalse(queue.player.playing)

        queue.play()
        self.assertTrue(queue.player.playing)
