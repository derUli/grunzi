import unittest

from utils.camera import Camera


class CameraTest(unittest.TestCase):
    def test_to_dict(self):
        self.assertEqual((123, 456), Camera(123, 456).to_dict())

    def test_to_list(self):
        self.assertEqual([123, 456], Camera(123, 456).to_list())
