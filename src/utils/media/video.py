""" Video playback utils  """
import logging
import os
import shutil

import cv2
from pyvidplayer2 import VideoPyglet, PostProcessing

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
    @param volume: The volume
    """
    if not video_supported():
        logging.info(label_value('Video', 'Playback not supported on this platform'))
        return None

    if not os.path.exists(path):
        logging.error(f"File {path} not found")
        return None

    return Video(path, interp=cv2.INTER_CUBIC, size=size)


class Video(VideoPyglet):
    def __init__(
            self,
            path: str,
            chunk_size=300,
            max_threads=1,
            max_chunks=1,
            post_process=PostProcessing.none,
            interp=cv2.INTER_LINEAR,
            use_pygame_audio=False,
            size=None,
            volume=None
    ):
        super().__init__(path, chunk_size, max_threads, max_chunks, post_process, interp, use_pygame_audio)

        if size is not None:
            self.resize(size)

        if volume is not None:
            self.set_volume(volume)
