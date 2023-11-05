""" KEYBOARD_MAPPINGS """
import pygame

K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT
K_UP = pygame.K_UP
K_DOWN = pygame.K_DOWN
K_DROP_ITEM = pygame.K_d
K_RUN = pygame.K_LSHIFT

K_TOGGLE_EDIT_MODE = pygame.K_F1
K_SAVE_LEVEL = pygame.K_F5
K_CHANGE_BLOCK_UP = pygame.K_PAGEUP
K_CHANGE_BLOCK_DOWN = pygame.K_PAGEDOWN

MOVEMENT_KEYS = [
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN
]

ABORT_KEYS = [
    pygame.K_ESCAPE
]

CONFIRM_KEYS = [
    pygame.K_SPACE,
    pygame.K_RETURN
]

NUMERIC_KEYS = [
    pygame.K_0,
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_0
]

DISCARD_KEYS = MOVEMENT_KEYS + CONFIRM_KEYS
