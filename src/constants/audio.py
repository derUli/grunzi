""" Audio constants """
from utils.path import is_windows, is_linux


def audio_backends() -> list:
    """
    Get supported audio backends
    @return: Supported audio backends
    """
    backends = [
        'auto'
    ]

    if is_windows():
        backends += [
            'xaudio2',
            'directsound'
        ]

    backends += ['openal']

    if is_linux():
        backends += ['pulse']

    backends += ['silent']

    return backends


# Default is autodetect
DEFAULT_AUDIO_BACKEND = audio_backends()[0]
