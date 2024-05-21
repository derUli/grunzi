""" Video playback utils  """
import logging
import os
import shutil

import cv2

try:
    from pyvidplayer2 import VideoPyglet
except AttributeError as e:
    logging.error(e)

from utils.path import is_windows
from utils.text import label_value


def has_ffmpeg() -> bool:
    """ Check if ffmpeg is in $PATH """
    return shutil.which('ffmpeg') is not None


def video_supported() -> bool:
    """ Video playback is currently only supported on Windows """
    return has_ffmpeg() and is_windows()


def load_video(
        path: str,
        size: tuple[int, int] | None = None,
        volume: float = 1
):
    """
    Load video from file

    @param path: The path
    @param size: The target size
    @param volume:

    """
    if not video_supported():
        logging.info(label_value('Video', 'Playback not supported on this platform'))
        return None

    if not os.path.exists(path):
        logging.error(f"File {path} not found")
        return None

    video = VideoPyglet(path, interp=cv2.INTER_CUBIC)

    if size:
        video.resize(size)

    video.set_volume(volume)

    return video
