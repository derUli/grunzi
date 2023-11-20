import os
import pygame
import shutil
from utils.path import get_userdata_path
from utils.animation import Animation

# BMP is the fastest image encoder supported by pygame.image.save()
STORED_EXTENSION = '.bmp'

def store_clear():
    cached_dir = os.path.join(get_userdata_path(), 'cached')
    if os.path.exists(cached_dir):
        shutil.rmtree(cached_dir)

def store_render(name, images, progress_callback = None):

    cached_dir = os.path.join(get_userdata_path(), 'cached', name)

    if not os.path.exists(cached_dir):
        os.makedirs(cached_dir)

    frame = 0
    one_percent = 100 / len(images)
    percent = 0

    if progress_callback:
        progress_callback(percent, _('Generating cache...'))

    for image in images:
        percent += one_percent
        # BMP, TGA, PNG, or JPEG
        path = os.path.join(cached_dir, str(frame).rjust(4, '0') + STORED_EXTENSION)

        pygame.image.save(image, path)
        frame += 1

        if progress_callback:
            progress_callback(percent, _('Generating cache...'))

    progress_callback(100, _('Generating cache...'))


def load_render(name, refresh_interval, start_frame=0, size=None, loop = True):
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
