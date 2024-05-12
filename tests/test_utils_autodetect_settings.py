import unittest

from constants.settings import SETTINGS_HIGH, SETTINGS_MEDIUM, SETTINGS_LOW
from utils.autodetectsettings.AutodetectSettings import AutodetectSettings
from utils.path import get_autodetect_path


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

    def test_arc(self):
        detector = AutodetectSettings(
            vendor='Intel',
            model='Mesa Intel(R) Arc(tm) A770 Graphics (DG2)'
        )

        self.assertEqual(SETTINGS_HIGH, detector.detect())

    def test_uhd(self):
        detector = AutodetectSettings(
            vendor='Intel',
            model='Intel(R) UHD Graphics'
        )

        self.assertEqual(SETTINGS_MEDIUM, detector.detect())

    def test_hd(self):
        detector = AutodetectSettings(
            vendor='Intel',
            model='Intel(R) HD Graphics'
        )

        self.assertEqual(SETTINGS_LOW, detector.detect())

    def test_radeon_6700(self):
        detector = AutodetectSettings(
            vendor='ATI Technologies Inc.',
            model='AMD Radeon RX 6700'
        )

        self.assertEqual(SETTINGS_HIGH, detector.detect())

    def test_unknown(self):
        detector = AutodetectSettings(
            vendor='Compu-Global-Hyper-Mega-Net',
            model='Potato'
        )

        self.assertEqual(SETTINGS_LOW, detector.detect())

    def test_save(self):
        detector = AutodetectSettings(
            vendor='NVIDIA Corporation',
            model='GeForce GTX 460/PCIe/SSE2'
        )

        detector.save()

        with open(get_autodetect_path(), 'r') as f:
            self.assertEqual('medium', f.read().strip())