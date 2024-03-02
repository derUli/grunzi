import re

from utils.netcode import get_own_ip

match = re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", "127.0.0.1")

import unittest



class PathTest(unittest.TestCase):
    def test_get_own_ip(self):
        self.assertEqual(3, get_own_ip().count('.'))