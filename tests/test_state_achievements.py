import unittest

from snapshottest import TestCase

from state.achievements import AchievementsState, Achievement, ACHIEVEMENT_CODE_CRACKER


class AchievementsStateTest(TestCase):
    def test_get_achievement_path(self):
        state = AchievementsState()

        self.assertTrue('achievements.json' in state.get_achievement_path())
        self.assertFalse('savegames' in state.get_achievement_path())

    def test_from_json(self):
        state = AchievementsState()
        state.load()
        state.load()

        self.assertFalse(state.achievements[ACHIEVEMENT_CODE_CRACKER].completed)
        state.from_json('{"code_cracker": {"completed": true}}')

        self.assertTrue(state.achievements[ACHIEVEMENT_CODE_CRACKER].completed)

    def test_to_json(self):
        state = AchievementsState()
        self.assertMatchSnapshot(state.to_json(), 'achievements_json')


class AchievementsTest(unittest.TestCase):
    def test_get_display_text(self):
        achievement = Achievement(ACHIEVEMENT_CODE_CRACKER)
        self.assertEqual('Code cracker', achievement.get_display_text())

    def test_from_dict(self):
        achievement = Achievement(ACHIEVEMENT_CODE_CRACKER)
        self.assertEqual(ACHIEVEMENT_CODE_CRACKER, achievement.achievement_id)

        self.assertFalse(achievement.completed)
        achievement.from_dict({'id': 'foo', 'completed': True})
        self.assertTrue(achievement.completed)
        self.assertEqual('foo', achievement.achievement_id)

    def test_to_dict(self):
        achievement = Achievement(ACHIEVEMENT_CODE_CRACKER)
        dict = achievement.to_dict()

        self.assertEqual(ACHIEVEMENT_CODE_CRACKER, dict['id'])
        self.assertFalse(dict['completed'])
