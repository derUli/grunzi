import pygame
def play_sound(file):
    pygame.mixer.Sound(file).play()