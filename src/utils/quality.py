import pygame
from constants.quality import QUALITY_VERY_LOW, QUALITY_HIGH

ENABLE_BLOOM = False
ENABLE_SMOOTH_SCALE = False
ENABLE_FONT_ANTIALIASING = False
SHADER_QUALITY = QUALITY_VERY_LOW
POST_PROCESSING = QUALITY_VERY_LOW

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

def postprocessing():
    """ Postprocessing enabled """
    return POST_PROCESSING > QUALITY_VERY_LOW

def postprocessing_high():
    return POST_PROCESSING >= QUALITY_HIGH

def pixel_fades_enabled():
    return shader_enabled()

def bloom_enabled():
    return POST_PROCESSING >= QUALITY_HIGH