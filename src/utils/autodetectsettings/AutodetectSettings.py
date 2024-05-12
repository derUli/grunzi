import logging
import re

from constants.settings import SETTINGS_HIGH, SETTINGS_LOW, SETTINGS_MEDIUM

# NVIDiA
MODEL_TYPE_RTX = 'RTX'
MODEL_TYPE_GTX = 'GTX'
MODEL_TYPE_GT = 'GT'

# INTEL
MODEL_TYPE_ARC = 'ARC'
MODEL_TYPE_HD = 'HD'
MODEL_TYPE_UHD = 'UHD'

VENDOR_NVIDIA = 'NVIDIA'
VENDOR_INTEL = 'INTEL'
VENDOR_AMD = 'AMD'
VENDOR_ATI = 'ATI'


class AutodetectSettings:
    def __init__(self, vendor, model):
        self.vendor = str(vendor).upper()
        self.model = str(model).upper()

    def detect(self):

        if VENDOR_NVIDIA in self.vendor:
            return self.detect_nvidia()

        if VENDOR_INTEL in self.vendor:
            return self.detect_intel()

        if VENDOR_AMD in self.vendor or VENDOR_ATI in self.vendor:
            return self.detect_amd()

        return SETTINGS_LOW

    def detect_nvidia(self):
        model_parts = re.findall("(GT|GTX|GTS|RTX)? (\d{3,4})", self.model)

        # If the GPU type can not be parsed return low
        if len(model_parts) == 0:
            return SETTINGS_LOW

        part1, part2 = list(model_parts[0])
        model_parts = [part1, part2]

        model_type = None
        model_number = 0

        if len(model_parts) >= 2:
            model_type = str(model_parts[0])

            if model_parts[1].isnumeric():
                model_number = int(model_parts[1])

        logging.info((model_type, model_number))

        # All RTX GPUs are strong enough to run this game
        if model_type == MODEL_TYPE_RTX:
            return SETTINGS_HIGH

        if model_type == MODEL_TYPE_GT:

            # My GT 1030 runs this game fine at high settings
            if model_number == 1030:
                return SETTINGS_HIGH

            # The GT 730 maybe runs this game at medium settings
            if 730 <= model_number <= 800:
                return SETTINGS_MEDIUM

        if model_type == MODEL_TYPE_GTX:
            # All GTX 600 Series and better can run this game at high settings
            if model_number >= 600:
                return SETTINGS_HIGH

            # All GTX 200 to 500 series should be able to run this game at medim settings
            if model_number >= 400:
                return SETTINGS_MEDIUM

        return SETTINGS_LOW

    def detect_intel(self):

        if MODEL_TYPE_ARC in self.model:
            return SETTINGS_HIGH

        if MODEL_TYPE_UHD in self.model:
            return SETTINGS_MEDIUM

        return SETTINGS_LOW

    def detect_amd(self):
        # I don't have any clue about AMD GPUs
        return SETTINGS_HIGH
