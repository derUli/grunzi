import logging
import os

from utils.path import get_userdata_path, is_windows

log_file = os.path.join(get_userdata_path(), 'debug.log')
file_handler = logging.FileHandler(log_file)

def configure_logger(log_level) -> None:
    """ Configure logger """
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[file_handler,
            logging.StreamHandler()
        ]
    )


def get_version(file: str) -> str:
    """ Get build number from VERSION file """

    # Fallback string if no VERSION exists
    text = 'Unknown Build'

    if not os.path.isfile(file):
        return text

    with open(file, 'r') as f:
        text = f.read()

    return text.strip()


def enable_high_dpi() -> bool:
    """
    Add support for high DPI on windows
    """
    # Abort if not windows
    if not is_windows():
        return False

    import ctypes

    try:
        # Set DPI Process aware
        ctypes.windll.user32.SetProcessDPIAware()
        logging.debug('SetProcessDPIAware')
    except AttributeError as e:
        # Windows XP doesn't support monitor scaling, so just do nothing
        logging.error(e)
        return False

    return True
