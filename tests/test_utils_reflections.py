import unittest
from pygame.time import Clock as clock_type

from utils.reflections import get_class, import_module, fullname
class ReflectionsTest(unittest.TestCase):
    def test_get_class(self):
        self.assertEqual(clock_type, get_class('pygame.time.Clock'))

    def test_get_class_fails(self):
        self.assertRaises(ImportError, self._get_class)

    def _get_class(self):
        get_class('hello.world')
    def test_fullname(self):
        self.assertEqual('pygame.time.Clock', fullname(clock_type()))

