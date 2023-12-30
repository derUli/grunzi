import os
import shutil

import pygame

from utils.animation import Animation
from utils.path import get_userdata_path

# BMP is the fastest image encoder supported by pygame.image.save()
STORED_EXTENSION = '.bmp'


def store_clear():
    """ Clear cache """
    cached_dir = os.path.join(get_userdata_path(), 'cached')
    if os.path.exists(cached_dir):
        shutil.rmtree(cached_dir)


def store_rendered_sequence(name, images, progress_callback=None):
    """ Store sequence """
    cached_dir = os.path.join(get_userdata_path(), 'cached', name)

    if not os.path.exists(cached_dir):
        os.makedirs(cached_dir)

    frame = 0
    one_percent = 100 / len(images)
    percent = 0

    if progress_callback:
        progress_callback(percent, _('Generating cache...'))

    for image in images:
        if isinstance(image, tuple):
            name, surface = image
        else:
            name = str(frame).rjust(4, '0')
            surface = image

        name += STORED_EXTENSION

        percent += one_percent
        # BMP, TGA, PNG, or JPEG
        path = os.path.join(cached_dir, name)

        pygame.image.save(surface, path)
        frame += 1

        if progress_callback:
            progress_callback(percent, _('Generating cache...'))

    progress_callback(100, _('Generating cache...'))


def load_rendered_sequence(name, refresh_interval, start_frame=0, size=None, loop=True):
    """ Load rendered sequence """
    cached_dir = os.path.join(get_userdata_path(), 'cached', name)

    if not os.path.exists(cached_dir):
        return None

    animation = Animation(
        cached_dir,
        refresh_interval=refresh_interval,
        start_frame=start_frame,
        size=size,
        loop=loop
    )

    if not len(animation.files):
        return None

    animation.load()
    return animation
