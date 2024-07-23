import unittest

from utils.keypressed import KeyPressed


class KeyPressedTest(unittest.TestCase):
    def test_reset(self):
        pressed = KeyPressed()

        pressed.key_right = True
        self.assertTrue(pressed.key_right)

        pressed.reset()
        self.assertFalse(pressed.key_right)
