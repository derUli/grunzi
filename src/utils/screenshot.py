import os
import time
import pygame
import logging

from utils.path import get_userdata_path


def make_screenshot(screen: pygame.surface.Surface) -> str:
    """ Save a screenshot """
    screenshot_dir = os.path.join(get_userdata_path(), 'screenshots')

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    output_file = os.path.join(
        screenshot_dir,
        time.strftime("%Y%m%d-%H%M%S") + '.jpg'
    )

    pygame.image.save(screen, output_file)

    logging.debug('Screenshot saved as ' + output_file)

    return output_file


def make_dump(screen: pygame.surface.Surface) -> None:
    """ Stores an image dump of the full map """
    screenshot_dir = os.path.join(get_userdata_path(), 'dumps')

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    output_file = os.path.join(
        screenshot_dir,
        time.strftime("%Y%m%d-%H%M%S") + '.jpg'
    )

    # This will take some time since the file is huge
    pygame.image.save(screen, output_file)

    logging.debug('Map image dumped as ' + output_file)

    return output_file
