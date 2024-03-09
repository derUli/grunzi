""" Video playback utils  """
import logging
import os
import shutil

try:
    from pyvidplayer2 import VideoPyglet
except Exception as e:
    logging.error(e)

from utils.path import is_windows


def load_video(
        path: str,
        size: tuple[int, int] | None = None,
        volume: float = 1
):
    has_ffmpeg = shutil.which('ffmpeg')

    if not has_ffmpeg:
        return None

    if not is_windows():
        logging.warning("Video play back isn't support on Linux currently")
        return

    if not os.path.exists(path):
        return None

    video = VideoPyglet(path)

    if size:
        video.resize(size)

    video.set_volume(volume)

    return video
