import pygame

ENABLE_SMOOTH_SCALE = False
ENABLE_FONT_ANTIALIASING = False
SHADER_ENABLED = False


def scale_method():
    """ Get scale method based on the current quality """
    if ENABLE_SMOOTH_SCALE:
        return pygame.transform.smoothscale

    return pygame.transform.scale


def font_antialiasing():
    """ Get fount antialiasing based on the current quality """
    return ENABLE_FONT_ANTIALIASING


def shader_enabled():
    return SHADER_ENABLED
