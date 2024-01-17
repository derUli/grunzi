""" Audio playback utilities  """

import logging

import pygame

# Used to show information about the sound output device
try:
    import pygame._sdl2.audio as sdl2_audio
except ImportError:
    sdl2_audio = None

# Current sound volume
SOUND_VOLUME = 1.0

CHANNELS = []


def play_sound(file: str) -> pygame.mixer.Channel:
    """
    Plays a sound file once

    @param file: The sound file to play
    @return: The channel
    """
    logging.debug(f'Play sound {file}')
    sound = pygame.mixer.Sound(file)
    sound.set_volume(SOUND_VOLUME)

    channel = sound.play()
    CHANNELS.append(channel)
    return channel


def stop_sounds() -> None:
    """
    Stops all sounds
    """
    for channel in CHANNELS:
        if channel and channel.get_busy():
            channel.stop()

    CHANNELS.clear()

    logging.debug('All sounds stopped')


def pause_sounds() -> None:
    """
    Pause all sounds
    """
    for channel in CHANNELS:
        if channel and channel.get_busy():
            channel.pause()

    logging.debug('All sounds paused')


def unpause_sounds() -> None:
    """
    Unpause all songs
    """
    for channel in CHANNELS:
        if channel and channel.get_busy():
            channel.unpause()

    logging.debug('All sounds continued')


def sounds_busy() -> bool:
    """
    Unpause all songs
    """
    for channel in CHANNELS:
        if channel and channel.get_busy():
            return True
        
    return False

def play_music(file: str, repeat: int = -1) -> None:
    """
    Plays a music file
    @param file: The music file to play
    @param repeat: The number of repeat
    """
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(repeat)

    logging.debug(f'Play Music {file} {str(repeat)} times')


def stop_music() -> None:
    """
    Stops the music
    """
    pygame.mixer.music.stop()


def get_devices(capture_devices: bool = False) -> list:
    """
    Gets all audio output devices
    @param capture_devices: If capture devices should be also returned
    @return: List of audio devices
    """
    pygame.init()

    devices = []

    if sdl2_audio:
        try:
            devices = list(sdl2_audio.get_audio_device_names(capture_devices))
        except pygame._sdl2.sdl2.error as e:
            logging.error(e)

    return devices
