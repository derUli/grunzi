import arcade
import unittest

from utils.log import configure_logger
from utils.scene import get_layer

configure_logger()


class TestUtilsScene(unittest.TestCase):
    def setUp(self):
        self.scene = arcade.Scene()

    def test_get_layer_returns_existing(self):
        for i in range(0, 3):
            self.scene.add_sprite(
                'foo',
                arcade.sprite.SpriteSolidColor(1, 1, arcade.csscolor.RED)
            )
        layer = get_layer('foo', self.scene)

        self.assertEqual(3, len(layer))

    def test_get_layer_returns_new(self):
        layer = get_layer('foo', self.scene)

        self.assertEqual(0, len(layer))
