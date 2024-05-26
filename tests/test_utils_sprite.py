import arcade
import os
import unittest

from state.viewstate import ViewState
from utils.sprite import tilemap_size, random_position


class UtilsSpriteTest(unittest.TestCase):
    def test_tilemap_size(self):
        root_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src'
        )
        state = ViewState(root_dir, map_name='map01')
        map = arcade.load_tilemap(os.path.join(state.map_dir, 'map01.tmx'))
        self.assertEqual((10880, 5120), tilemap_size(map))

    def test_random_position(self):
        root_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src'
        )
        state = ViewState(root_dir, map_name='map01')
        map = arcade.load_tilemap(os.path.join(state.map_dir, 'map01.tmx'))

        old_x, old_y = random_position(map)
        self.assertGreaterEqual(old_x, 0)
        self.assertGreaterEqual(old_y, 0)
        self.assertLessEqual(old_x, 10880)
        self.assertLessEqual(old_y, 5120)

        self.assertNotEqual(random_position(map), random_position(map))
