import unittest

from utils.utils import natural_keys


class UtilsTest(unittest.TestCase):

    def test_natural_keys(self):
        alist = ['test10', 'test02', 'test2', 'test002', 'test1', 'test01', 'test1']
        alist.sort(key=natural_keys)

        self.assertEqual(
            ['test1', 'test01', 'test1', 'test02', 'test2', 'test002', 'test10'],
            alist

        )
