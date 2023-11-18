import unittest

from utils.helper import get_version
import os
class HelperTest(unittest.TestCase):
    def test_get_version1(self):
        self.assertEqual('Unknown Build', get_version('foo'))

    def test_get_version2(self):
        file = os.path.join(
            os.path.dirname(__file__),
            'VERSION',
        )

        self.assertEqual('1.0 Beta', get_version(file))