import pygame

ENABLE_SMOOTH_SCALE = False

ENABLE_FONT_ANTIALIASING = False

def scale_method():
    """ Get scale method based on the current quality"""
    if ENABLE_SMOOTH_SCALE:
        return pygame.transform.smoothscale

    return pygame.transform.scale

def font_antialiasing():
    return ENABLE_FONT_ANTIALIASING