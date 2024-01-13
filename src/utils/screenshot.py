import logging
import os
import time

import pygame

from utils.path import get_userdata_path

SCREENSHOT_DIR = 'screenshots'
DUMP_DIR = 'dumps'

def make_screenshot(screen: pygame.surface.Surface, target: str = SCREENSHOT_DIR) -> str:
    """ Save a screenshot """
    screenshot_dir = os.path.join(get_userdata_path(), target)

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    output_file = os.path.join(
        screenshot_dir,
        time.strftime("%Y%m%d-%H%M%S") + '.jpg'
    )

    pygame.image.save(screen, output_file)

    logging.debug('Screenshot saved as ' + output_file)

    return output_file
