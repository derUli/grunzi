import os
import unittest

from state.savegamestate import SaveGameState, new_savegame
from utils.path import get_settings_path


class SaveGameStateTest(unittest.TestCase):

    def test_exists(self):
        self.assertIsInstance(SaveGameState.exists(), bool)

    def test_get_selectable_empty(self):
        state = SaveGameState()
        state.current = 'map01'

        self.assertEqual(['map01'], state.get_selectable())

    def test_get_selectable_completed(self):
        state = SaveGameState()
        state.completed = ['map01', 'map02']
        state.current = 'map03'

        self.assertEqual(['map01', 'map02', 'map03'], state.get_selectable())


    def test_load(self):
        self.assertIsInstance(SaveGameState.load(), SaveGameState)

    def test_save(self):
        SaveGameState.load().save()

        self.assertTrue(os.path.exists(get_settings_path()))

    def test_new_savegame(self):
        self.assertIsInstance(new_savegame('map01'), SaveGameState)