import logging
import os
import unittest

from utils.helper import get_version, enable_high_dpi, configure_logger


class HelperTest(unittest.TestCase):
    def test_get_version1(self):
        self.assertEqual('Unknown Build', get_version('foo'))

    def test_get_version2(self):
        file = os.path.join(
            os.path.dirname(__file__),
            'VERSION',
        )

        self.assertEqual('1.0 Beta', get_version(file))

    def test_enable_high_dpi(self):
        enable_high_dpi()
        self.assertEqual('permonitorv2', os.environ['SDL_WINDOWS_DPI_AWARENESS'])

    def test_configure_logger(self):
        configure_logger(logging.DEBUG)
        self.assertTrue(any(logging.getLogger().handlers))

        for handler in logging.getLogger().handlers:
            self.assertIsInstance(handler, logging.StreamHandler)

            if isinstance(handler, logging.FileHandler):
                handler.close()
