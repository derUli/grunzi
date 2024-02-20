import unittest

from state.achievements import AchievementsState, Achievement
from snapshottest import TestCase

class AchievementsStateTest(TestCase):
    def test_get_achievement_path(self):
        state = AchievementsState()

        self.assertTrue('achievements.json' in state.get_achievement_path())
        self.assertFalse('savegames' in state.get_achievement_path())

    def test_from_json(self):
        state = AchievementsState()
        self.assertFalse(state.achievements['code_cracker'].completed)
        state.from_json('{"code_cracker": {"completed": true}}')

        self.assertTrue(state.achievements['code_cracker'].completed)
    def test_to_json(self):
        state = AchievementsState()
        self.assertMatchSnapshot(state.to_json(), 'achievements_json')

class AchievementsTest(unittest.TestCase):
    def test_get_display_text(self):
        achievement = Achievement('code_cracker')
        self.assertEqual('Code cracker', achievement.get_display_text())

    def test_from_dict(self):
        achievement = Achievement('code_cracker')
        self.assertEqual('code_cracker', achievement.achievement_id)

        self.assertFalse(achievement.completed)
        achievement.from_dict({'id': 'foo', 'completed': True})
        self.assertTrue(achievement.completed)
        self.assertEqual('foo', achievement.achievement_id)

    def test_to_dict(self):
        achievement = Achievement('code_cracker')
        dict = achievement.to_dict()

        self.assertEqual('code_cracker', dict['id'])
        self.assertFalse(dict['completed'])