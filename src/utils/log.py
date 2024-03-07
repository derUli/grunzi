""" Logging utilities """

import logging
import os
import platform
import sys
from logging.handlers import RotatingFileHandler

import arcade
import sounddevice
import psutil

from . import path

log_file = os.path.join(path.get_userdata_path(), 'debug.log')
if not os.path.exists(path.get_userdata_path()):
    os.makedirs(path.get_userdata_path())

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


def log_hardware_info() -> None:
    """
    Log hardware info
    """
    uname = platform.uname()
    logging.info(f"OS: {uname.system} {uname.version}")
    logging.info(f"CPU: {uname.processor}")
    logging.info(f"RAM: {round(psutil.virtual_memory().total / 1024 / 1024)} MB")

    window = arcade.Window(visible=False)
    ctx = window.ctx

    logging.info(f"GPU: {ctx.info.RENDERER}")

    for audio in sounddevice.query_devices():
        logging.info(f"Audio: {audio['name']}")

    window.close()
