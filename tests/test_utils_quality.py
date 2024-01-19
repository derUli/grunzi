import unittest

import constants.quality
import utils.quality as quality
from state.settingsstate import SettingsState


class QualityTest(unittest.TestCase):
    def setUp(self):
        quality.settings_state = SettingsState()

    def test_scale_method(self):
        quality.settings_state.smoothscale = True
        # TODO: How to check if this is callable method
        self.assertEqual('<built-in function smoothscale>', str(quality.scale_method()))

        quality.settings_state.smoothscale = False
        self.assertEqual('<built-in function scale>', str(quality.scale_method()))

    def test_font_antialiasing_enabled(self):
        self.assertTrue(quality.font_antialiasing_enabled())

    def test_shader_enabled(self):
        self.assertTrue(quality.shader_enabled())

    def test_pixel_fades_enabled(self):
        self.assertTrue(quality.pixel_fades_enabled())

    def test_filmgrain_enabled(self):
        self.assertTrue(quality.filmgrain_enabled())

    # def test_daynightcycle_enabled(self):
        #self.assertTrue(quality.daynightcycle_enabled())

    def test_fog_enabled(self):
        quality.settings_state.fog = False
        self.assertFalse(quality.fog_enabled())

        quality.settings_state.fog = True
        self.assertTrue(quality.fog_enabled())

    def test_bloom_enabled(self):
        quality.settings_state.bloom = False
        self.assertFalse(quality.bloom_enabled())

        quality.settings_state.bloom = True
        self.assertTrue(quality.bloom_enabled())

    def test_blood_enabled_medium(self):
        quality.settings_state.blood = constants.quality.QUALITY_MEDIUM

        self.assertTrue(quality.blood_enabled())
        self.assertFalse(quality.blood_enabled_high())

    def test_blood_enabled_high(self):
        quality.settings_state.blood = constants.quality.QUALITY_HIGH

        self.assertTrue(quality.blood_enabled())
        self.assertTrue(quality.blood_enabled_high())

    def test_weather_enabled(self):
        quality.settings_state.weather = constants.quality.QUALITY_MEDIUM
        self.assertTrue(quality.weather_enabled())


    def test_weather_enabled_high(self):
        quality.settings_state.weather = constants.quality.QUALITY_HIGH
        self.assertEqual(constants.quality.QUALITY_HIGH, quality.weather_quality())