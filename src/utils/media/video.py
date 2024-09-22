""" Video playback utils  """
import logging
import os
import shutil
from typing import Tuple

import cv2
import numpy
from pyvidplayer2 import VideoPyglet

from utils.text import label_value


def has_ffmpeg() -> bool:
    """ Check if ffmpeg is in $PATH """

    return shutil.which('ffmpeg') is not None


def video_supported() -> bool:
    """ Video playback is currently only supported on Windows """

    try:
        import pyvidplayer2

        info = pyvidplayer2.get_version_info()
        logging.info(info)
        return len(info['ffmpeg']) >= 1

    except ImportError as e:
        logging.error(e)

        return False


def load_video(
        path: str,
        size: tuple[int, int] | None = None,
        volume: float = 1
):
    """
    Load video from file

    @param path: The path
    @param size: The target size
    @param volume: The volume
    """

    if not video_supported():
        logging.info(label_value('Video', 'Playback not supported on this platform'))
        return Video(None, interp=cv2.INTER_CUBIC, size=size)

    if not os.path.exists(path):
        logging.error(f"File {path} not found")
        return Video(None, interp=cv2.INTER_CUBIC, size=size)

    return Video(path, interp=cv2.INTER_CUBIC, size=size, volume=volume)


if not video_supported():
    class VideoPyglet:
        pass


class Video(VideoPyglet):
    def __init__(
            self,
            path: str | None = None,
            chunk_size: int = 300,
            max_threads: int = 1,
            max_chunks: int = 1,
            interp: int = cv2.INTER_LINEAR,
            use_pygame_audio: bool = False,
            size: Tuple[int, int] | None = None,
            volume: float | None = None
    ):
        self.path = path
        self.active = False

        if path:
            super().__init__(path, chunk_size, max_threads, max_chunks, post_process, interp, use_pygame_audio)

        if size is not None:
            self.resize(size)

        if volume is not None:
            self.set_volume(volume)
