import unittest

from constants.settings import QualityPreset, DEFAULT_FILMGRAIN


class SettingsTest(unittest.TestCase):
    def test_preset_highest(self):
        preset = QualityPreset(6)

        self.assertEqual(preset.antialiasing, 16)
        self.assertTrue(preset.color_tint)
        self.assertEqual(preset.filmgrain, DEFAULT_FILMGRAIN)
        self.assertTrue(preset.fog)

    def test_preset_lowest(self):
        preset = QualityPreset(0)

        self.assertEqual(preset.antialiasing, 0)
        self.assertFalse(preset.color_tint)
        self.assertEqual(preset.filmgrain, 0.0)
        self.assertFalse(preset.fog)
