import unittest

from constants.direction import key_to_direction, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_DOWN, DIRECTION_LEFT
from constants.keyboard import K_RIGHT, K_UP, K_DOWN, K_LEFT


class DirectionTest(unittest.TestCase):
    def test_direction(self):
        self.assertEqual(DIRECTION_UP, key_to_direction(K_UP[0]))
        self.assertEqual(DIRECTION_RIGHT, key_to_direction(K_RIGHT[0]))
        self.assertEqual(DIRECTION_DOWN, key_to_direction(K_DOWN[0]))
        self.assertEqual(DIRECTION_LEFT, key_to_direction(K_LEFT[0]))
