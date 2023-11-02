import pygame


def play_sound(file):
    pygame.mixer.Sound(file).play()


def play_music(file, repeat=-1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(repeat)


def stop_music():
    pygame.mixer.music.stop()
