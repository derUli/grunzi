import unittest

from utils.highscore import HighscoreStorage


class UtilsHighscoreTest(unittest.TestCase):

    def test_fetch(self):
        storage = HighscoreStorage()
        self.assertTrue(storage.fetch())

        self.assertIsInstance(storage.highscore, list)

        for score in storage.highscore:
            self.assertIsInstance(score['name'], str)
            self.assertIsInstance(score['score'], int)
            self.assertGreaterEqual(len(score['name']), 1)
