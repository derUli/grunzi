import unittest

from utils.helper import get_version
class HelperTest(unittest.TestCase):
    def test_direction(self):

        self.assertEqual('Unknown Build', get_version('foo'))