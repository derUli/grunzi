import unittest

from utils.camera import Camera


class CameraTest(unittest.TestCase):
    def test_to_dict(self):
        self.assertEqual((123, 456), Camera(123, 456).to_dict())

    def test_to_list(self):
        self.assertEqual([123, 456], Camera(123, 456).to_list())

    def test_update(self):
        camera = Camera(12, 34)

        camera.update(-2, -2)

        self.assertEqual([0, 0], camera.to_list())
