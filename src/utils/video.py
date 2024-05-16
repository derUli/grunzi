""" Video playback utils  """
import logging
import os
import shutil

from pyvidplayer2 import VideoPyglet

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
    """ Load video from file """
    if not video_supported():
        logging.info(label_value('Video', 'Playback not supported on this platform'))
        return

    if not os.path.exists(path):
        logging.error('Video', f"File {path} not found")
        return None

    video = VideoPyglet(path)

    if size:
        video.resize(size)

    video.set_volume(volume)

    return video
