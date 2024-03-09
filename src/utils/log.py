""" Logging utilities """

import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler

import psutil
import pyglet

try:
    import sounddevice
except ImportError:
    sounddevice = None

from .path import get_log_path
from .text import label_value

log_file = os.path.join(get_log_path(), 'debug.log')

file_handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=5 * 1024 * 1024,  # Maximum log file size 5 MB
    # Keep previous 3 log files
    backupCount=3,
)
stdout_handler = logging.StreamHandler(stream=sys.stdout)

handlers = [file_handler, stdout_handler]


def configure_logger(log_level: int | str = logging.INFO) -> None:
    """ Configure logger
    @param log_level: Log level
    """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )


def log_hardware_info(window) -> None:
    """
    Log hardware info
    """

    # Log OS info
    uname = platform.uname()
    logging.info(label_value('OS', f"{uname.system} {uname.version}"))

    # Log CPU model
    logging.info(label_value('CPU', uname.processor))

    # Log the ram size
    ram_size = round(psutil.virtual_memory().total / 1024 / 1024 / 1024)
    logging.info(label_value('RAM', f"{ram_size} GB"))

    # Renderer is the GPU
    logging.info(label_value('GPU VENDOR', window.ctx.info.VENDOR))
    logging.info(label_value('GPU RENDERER', window.ctx.info.RENDERER))
    logging.info(label_value('GPU MAX_TEXTURE_SIZE', window.ctx.info.MAX_TEXTURE_SIZE))

    logging.info(label_value('OpenGL version', pyglet.gl.gl_info.get_version_string()))

    if not sounddevice:
        logging.info(label_value('Audio', 'Unknown'))
        return

    # Log the audio devices
    for audio in sounddevice.query_devices():
        logging.info(label_value('Audio', audio['name']))
