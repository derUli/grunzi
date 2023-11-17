import pygame

ENABLE_SMOOTH_SCALE = False
ENABLE_FONT_ANTIALIASING = False
SHADER_ENABLED = False
VIGNETTE_ENABLED = False
PIXEL_FADES = False


def scale_method():
    """ Get scale method based on the current quality """
    if ENABLE_SMOOTH_SCALE:
        return pygame.transform.smoothscale

    return pygame.transform.scale


def font_antialiasing_enabled():
    """ Get fount antialiasing based on the current quality """
    return ENABLE_FONT_ANTIALIASING


def shader_enabled():
    return SHADER_ENABLED


def vignette_enabled():
    return VIGNETTE_ENABLED


def pixel_fades_enabled():
    return PIXEL_FADES
