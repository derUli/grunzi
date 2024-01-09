import pygame
from constants.quality import QUALITY_OFF, QUALITY_VERY_LOW, QUALITY_LOW, QUALITY_MEDIUM, QUALITY_HIGH, QUALITY_VERY_HIGH, QUALITY_EXTREME

ENABLE_SMOOTH_SCALE = False
ENABLE_FONT_ANTIALIASING = True
SHADER_QUALITY = QUALITY_OFF
PIXEL_FADES = False
POST_PROCESSING = QUALITY_OFF


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
    return SHADER_QUALITY > QUALITY_OFF


def film_grain():
    """ Postprocessing enabled """
    return POST_PROCESSING >= QUALITY_VERY_LOW


def daynightcycle_enabled():
    """ Postprocessing enabled """
    return POST_PROCESSING >= QUALITY_LOW

    
def fog_enabled():
    """ Postprocessing enabled """
    return POST_PROCESSING >= QUALITY_VERY_HIGH


def pixel_fades_enabled():
    return shader_enabled()


def bloom_enabled():
    return POST_PROCESSING >= QUALITY_EXTREME


def blood_enabled():
    return POST_PROCESSING >= QUALITY_MEDIUM


def blood_enabled_high():
    return POST_PROCESSING >= QUALITY_HIGH
