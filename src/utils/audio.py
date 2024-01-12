import logging

import pygame

try:
    import pygame._sdl2.audio as sdl2_audio
except ImportError:
    sdl2_audio = None

sound_volume = 1.0

CHANNELS = []


def play_sound(file: str) -> pygame.mixer.Channel:
    logging.debug('Play sound ' + file)
    """ Play a sound once """
    sound = pygame.mixer.Sound(file)
    sound.set_volume(sound_volume)

    channel = sound.play()
    CHANNELS.append(channel)
    return channel


def stop_sounds() -> None:
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
