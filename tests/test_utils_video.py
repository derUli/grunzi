import os
import unittest

from utils.video import load_video


class VideoTest(unittest.TestCase):

    def setUp(self):
        # extend path for ffmpeg
        thirdpartydir = os.path.abspath(
            os.path.join('..', 'src', 'data', '3rdparty')
        )
        os.environ["PATH"] += os.pathsep + thirdpartydir

    def test_load_video(self):
        path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src',
            'data',
            'videos',
            'splash',
            'map01.webm'
        )

        video = load_video(path, (640, 480), True)

        self.assertEqual(video.path, path)
        self.assertTrue(video.current_size, (640, 480))
        self.assertFalse(video.muted)
