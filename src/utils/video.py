
""" Video playback utils  """
import os
import shutil

from pyvidplayer2 import VideoPyglet


def load_video(path: str, size: tuple[int, int] | None = None, silent: bool = False) -> VideoPyglet | None:
    has_ffmpeg = shutil.which('ffmpeg')

    if not has_ffmpeg:
        return None

    if not os.path.exists(has_ffmpeg):
        return None

    video = VideoPyglet(path)

    if size:
        video.resize(size)

    if silent:
        video.mute()

    return video
