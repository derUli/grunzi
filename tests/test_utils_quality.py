import unittest


from utils.quality import scale_method, font_antialiasing_enabled, shader_enabled, vignette_enabled
class QualityTest(unittest.TestCase):
    def test_scale_method(self):
        self.assertEqual('<built-in function scale>' , str(scale_method()))

    def test_font_antialiasing_enabled(self):
        self.assertFalse(font_antialiasing_enabled())

    def shader_enabled(self):
        self.assertFalse(shader_enabled())

    def vignette_enabled(self):
        self.assertFalse(vignette_enabled())

