import os
import unittest

from constants.maps import FIRST_MAP
from state.viewstate import ViewState


class ViewStateTest(unittest.TestCase):
    def test_play_sound(self):
        root_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src'
        )
        state = ViewState(root_dir, map_name=FIRST_MAP)
        state.preload_sounds()
        state.play_sound('coin')
        self.assertTrue(state.sounds['coin'].is_playing)
