import unittest

from constants.settings import SETTINGS_HIGH, SETTINGS_MEDIUM, SETTINGS_LOW
from utils.autodetectsettings.AutodetectSettings import AutodetectSettings


class AutoDetectSettingsTest(unittest.TestCase):
    def test_nvidia_gt_1030(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='NVIDIA GeForce GT 1030/PCIe/SSE2'
        )

        self.assertEqual(SETTINGS_HIGH, detector.detect())

    def test_nvidia_gt_730(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='NVIDIA GeForce GT 730/PCIe/SSE2'
        )

        self.assertEqual(SETTINGS_MEDIUM, detector.detect())

    def test_nvidia_gt_610(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='NVIDIA GeForce GT 610/PCIe/SSE2'
        )

        self.assertEqual(SETTINGS_LOW, detector.detect())

    def test_nvidia_rtx_4070(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='NVIDIA GeForce RTX 4070/PCIe/SSE2'
        )

        self.assertEqual(SETTINGS_HIGH, detector.detect())

    def test_nvidia_gtx_1650(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='NVIDIA GeForce GTX 1650/PCIe/SSE2'
        )

        self.assertEqual(SETTINGS_HIGH, detector.detect())

    def test_nvidia_gtx_1650(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='NVIDIA GeForce GTX 1650/PCIe/SSE2'
        )

        self.assertEqual(SETTINGS_HIGH, detector.detect())

    def test_gtx_460(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='GeForce GTX 460/PCIe/SSE2'
        )

        self.assertEqual(SETTINGS_MEDIUM, detector.detect())

    def test_none(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='Foobar'
        )

        self.assertEqual(SETTINGS_LOW, detector.detect())
