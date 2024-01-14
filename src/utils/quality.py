from typing import Callable

import pygame

from constants.quality import QUALITY_MEDIUM, QUALITY_HIGH

settings_state = None


def scale_method() -> Callable:
    """ Get scale method based on video settings """
    if settings_state.smoothscale:
        return pygame.transform.smoothscale

    return pygame.transform.scale


def font_antialiasing_enabled() -> bool:
    """ Get fount antialiasing based on the current quality """
    return True


def shader_enabled() -> bool:
    """ Check shader enabled """
    return True


def filmgrain_enabled() -> bool:
    """ Check filmgrain enabled """
    return True


def daynightcycle_enabled() -> bool:
    """ Check day/night Cycle enabled """
    return True


def fog_enabled() -> bool:
    """ Check fog enabled """
    return settings_state and settings_state.fog

def snow_enabled() -> bool:
    return False

def pixel_fades_enabled() -> bool:
    """ Check fixel fades enabled """
    return shader_enabled()


def bloom_enabled() -> bool:
    """" Check bloom enabled"""
    return settings_state and settings_state.bloom


def blood_enabled() -> bool:
    """ Check blood (medium) is enabled """
    return settings_state and settings_state.blood >= QUALITY_MEDIUM


def blood_enabled_high() -> bool:
    """ Check blood (high) is enabled """
    return settings_state and settings_state.blood >= QUALITY_HIGH
