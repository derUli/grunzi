import unittest


from constants.keyboard import K_RIGHT
from constants.direction import key_to_direction, DIRECTION_RIGHT
class DirectionTest(unittest.TestCase):
    def test_direction(self):
        self.assertEqual(DIRECTION_RIGHT, key_to_direction(K_RIGHT[0]))