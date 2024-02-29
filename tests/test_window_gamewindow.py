import unittest

from window.gamewindow import GameWindow


class MyTestCase(unittest.TestCase):
    def test_size(self):
        window = GameWindow(window=True, width=800, height=600)
        self.assertEqual((800, 600), window.size())
