import pygame

ENABLE_SMOOTH_SCALE = False

def scale_method():
    print(ENABLE_SMOOTH_SCALE)
    if ENABLE_SMOOTH_SCALE:
        return pygame.transform.smoothscale

    return pygame.transform.scale