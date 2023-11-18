import pygame

sound_volume = 1.0


def play_sound(file):
    sound = pygame.mixer.Sound(file)
    sound.set_volume(sound_volume)
    return sound.play()


def play_music(file, repeat=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(repeat)

def stop_music():
    pygame.mixer.music.stop()
