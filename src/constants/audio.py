""" Audio constants """

# Audio backends supported by Pyglet
AUDIO_BACKENDS = [
    'auto',
    'xaudio2',
    'directsound',
    'openal',
    'pulse',
    'silent'
]

# Default is autodetect
DEFAULT_AUDIO_BACKEND = 'auto'
