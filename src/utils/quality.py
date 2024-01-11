import pygame
from constants.quality import QUALITY_MEDIUM, QUALITY_HIGH

settings_state = None


def scale_method():
    """ Get scale method based on video settings """
    if settings_state.smoothscale:
        return pygame.transform.smoothscale

    return pygame.transform.scale


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
    """ Fog enabled """
    return settings_state and settings_state.fog


def pixel_fades_enabled():
    """ Check if fixel fades are enabled """
    return shader_enabled()


def bloom_enabled():
    """ Too much demanding make it optional """
    return settings_state and settings_state.bloom


def blood_enabled():
    """ Blood is enabled """
    return settings_state and settings_state.blood >= QUALITY_MEDIUM


def blood_enabled_high():
    """ High quality blood is enabled """
    return settings_state and settings_state.blood >= QUALITY_HIGH
