import pygame

try:
    import pygame._sdl2.audio as sdl2_audio
except ImportError:
    sdl2_audio = None

sound_volume = 1.0

CHANNELS = []

def play_sound(file):
    """ Play a sound once """
    sound = pygame.mixer.Sound(file)
    sound.set_volume(sound_volume)

    channel = sound.play()
    CHANNELS.append(channel)
    return channel

def stop_sounds():
    for channel in CHANNELS:
        if channel and channel.get_busy():
            channel.stop()

    CHANNELS.clear()

def pause_sounds():
    for channel in CHANNELS:
        if channel and channel.get_busy():
            channel.pause()

def unpause_sounds():
    for channel in CHANNELS:
        if channel and channel.get_busy():
            channel.unpause()


def play_music(file, repeat=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(repeat)


def stop_music():
    pygame.mixer.music.stop()


def get_devices(capture_devices=False):
    pygame.init()
    if not sdl2_audio:
        return []
    devices = list(sdl2_audio.get_audio_device_names(capture_devices))

    return devices
