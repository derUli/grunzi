""" Screenshot tools """
import arcade
import logging
import os
import time

from utils.path import get_userdata_path


def make_screenshot():
    """ Save a screenshot
        @return: filename of the screenshot
    """
    screenshot_dir = os.path.join(get_userdata_path(), 'screenshots')

    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    filename = os.path.join(
        screenshot_dir,
        time.strftime("%Y%m%d-%H%M%S") + '.jpg'
    )

    start = time.time()
    image = arcade.get_image().convert('RGB')
    image.save(filename, quality=90)
    end = time.time() - start

    logging.debug(f"Screenshot saved as {filename} in {end} seconds")

    return filename
