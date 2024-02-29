""" Logging utilities """

import os
import sys

import logging
from utils.path import get_userdata_path

log_file = os.path.join(get_userdata_path(), 'debug.log')
if not os.path.exists(get_userdata_path()):
    os.makedirs(get_userdata_path())

file_handler = logging.FileHandler(filename=log_file)
stdout_handler = logging.StreamHandler(stream=sys.stdout)

handlers = [file_handler, stdout_handler]


def configure_logger(log_level) -> None:
    """ Configure logger """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
