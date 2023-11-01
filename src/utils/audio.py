import pygame
import constants.sound


def play_sound(file):
    pygame.mixer.Sound(file).play()


def play_music(file, repeat = -1):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(repeat)


def fadeout_music():
    pygame.mixer.music.fadeout(constants.sound.MUSIC_FADEOUT_TIME)


def stop_music():
    pygame.mixer.music.stop()
