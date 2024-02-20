import os.path
import unittest

from utils.savegame import build_savegame_directory_path, build_savegame_state_path, build_savegame_level_path, \
    has_savegames


class SavegameTest(unittest.TestCase):
    def test_build_savegame_directory_path(self):
        self.assertTrue(
            build_savegame_directory_path('foo').endswith(os.path.sep.join(['savegames', 'foo']))
        )

    def test_build_savegame_state_path(self):
        self.assertTrue(
            build_savegame_state_path('foo').
            endswith(
                os.path.sep.join(['savegames', 'foo', 'state.json'])
            )
        )

    def test_build_savegame_level_path(self):
        self.assertTrue(
            build_savegame_level_path('foo').
            endswith(
                os.path.sep.join(['savegames', 'foo', 'level.json'])
            )
        )

    def test_has_savegames(self):
        self.assertEqual(bool, type((has_savegames())))
