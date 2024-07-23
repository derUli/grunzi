import time
import unittest

from utils.fpscounter import FPSCounter


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
