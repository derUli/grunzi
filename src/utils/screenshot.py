import os
import time

import pygame

from utils.path import get_userdata_path


def make_screenshot(screen):
    screenshot_dir = os.path.join(get_userdata_path(), 'screenshots')

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    screenshot_file = os.path.join(
        screenshot_dir,
        time.strftime("%Y%m%d-%H%M%S") + '.jpg'
    )

    pygame.image.save(screen, screenshot_file)
