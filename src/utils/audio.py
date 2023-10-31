import pygame
import constants.sound

def play_sound(file):
    pygame.mixer.Sound(file).play()

def play_music(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)

def fadeout_music():
    pygame.mixer.music.fadeout(constants.sound.MUSIC_FADEOUT_TIME)