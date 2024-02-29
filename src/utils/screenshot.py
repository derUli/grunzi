import os
import time

import pyglet

import logging
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
        time.strftime("%Y%m%d-%H%M%S") + '.png'
    )

    start = time.time()
    buffer = pyglet.image.get_buffer_manager().get_color_buffer()
    buffer.save(filename)
    end = time.time() - start
    logging.debug(f"Screenshot saved as {filename} in {end} seconds")

    return filename
