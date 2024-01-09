import pygame
from constants.quality import QUALITY_OFF, QUALITY_HIGH, QUALITY_VERY_HIGH

settings_state = None

def scale_method():
    return pygame.transform.smoothscale


def font_antialiasing_enabled():
    """ Get fount antialiasing based on the current quality """
    return True


def shader_enabled():
    """ Get shader enabled """
    return True


def film_grain():
    """ Filmgrain enabled """
    return True


def daynightcycle_enabled():
    """ Daynight Cycle enabled """
    return True

    
def fog_enabled():
    """ Too much demanding, make it optional """
    return False


def pixel_fades_enabled():
    return shader_enabled()


def bloom_enabled():
    """ Too much demanding make it optional """
    return settings_state and settings_state.bloom


def blood_enabled():
    return settings_state and settings_state.blood >= QUALITY_HIGH


def blood_enabled_high():
    return settings_state and settings_state.blood >= QUALITY_VERY_HIGH
