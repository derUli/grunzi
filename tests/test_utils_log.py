import os
import time
import unittest

import arcade

from utils.log import configure_logger, log_hardware_info
from utils.path import get_userdata_path, get_log_path

configure_logger()

import logging


class TestUtilsLog(unittest.TestCase):
    def setUp(self):
        self.log_file = os.path.join(get_log_path(), 'debug.log')

    def test_configure_logger(self):
        timestamp_string = f"Test {time.time()}"

        logging.info(timestamp_string)

        with open(self.log_file, "r") as f:
            self.assertIn(timestamp_string, f.read())

    def test_log_hardware_info(self):
        window = arcade.Window(800, 600, visible=False)
        log_hardware_info(window)

        with open(self.log_file, "r") as f:
            logged = f.read()
            self.assertIn('[INFO] OS:', logged)
            self.assertIn('[INFO] CPU:', logged)
            self.assertIn('[INFO] RAM:', logged)
            self.assertIn('[INFO] GPU', logged)
