import pygame
from constants.quality import QUALITY_VERY_LOW, QUALITY_HIGH
ENABLE_SMOOTH_SCALE = False
ENABLE_FONT_ANTIALIASING = False
SHADER_QUALITY = QUALITY_VERY_LOW
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
    """ Get shader enabled """
    return SHADER_QUALITY > QUALITY_VERY_LOW

def shader_quality_high():
    """ Get quality high """
    return SHADER_QUALITY >= QUALITY_HIGH

def vignette_enabled():
    """ Vignette enabled """
    return shader_enabled()

def vignette_quality_high():
    return shader_quality_high()

def pixel_fades_enabled():
    return shader_enabled()


