import os
import unittest

import arcade

from state.viewstate import ViewState
from utils.sprite import tilemap_size, random_position


class UtilsSpriteTest(unittest.TestCase):
    def test_tilemap_size(self):
        root_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src'
        )
        state = ViewState(root_dir, map_name='empty')
        map = arcade.load_tilemap(os.path.join(state.map_dir, 'empty.tmx'))
        self.assertEqual((3200, 3200), tilemap_size(map))

    def test_random_position(self):
        root_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src'
        )
        state = ViewState(root_dir, map_name='empty')
        map = arcade.load_tilemap(os.path.join(state.map_dir, 'empty.tmx'))

        old_x, old_y = random_position(map)
        self.assertGreaterEqual(old_x, 0)
        self.assertGreaterEqual(old_y, 0)
        self.assertLessEqual(old_x, 3200)
        self.assertLessEqual(old_y, 3200)

        self.assertNotEqual(random_position(map), random_position(map))
