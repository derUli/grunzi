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
    logging.debug('Play sound ' + file)
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


def pause_sounds() -> None:
    for channel in CHANNELS:
        if channel and channel.get_busy():
            channel.pause()


def unpause_sounds() -> None:
    for channel in CHANNELS:
        if channel and channel.get_busy():
            channel.unpause()


def play_music(file, repeat=-1) -> None:
    logging.debug('Play music ' + file)
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(repeat)


def stop_music() -> None:
    pygame.mixer.music.stop()


def get_devices(capture_devices: bool = False) -> list:
    pygame.init()
    if not sdl2_audio:
        return []
    devices = list(sdl2_audio.get_audio_device_names(capture_devices))

    return devices
