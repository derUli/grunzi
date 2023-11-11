""" KEYBOARD_MAPPINGS """
import pygame

K_LEFT = [pygame.K_LEFT, pygame.K_a]
K_RIGHT = [pygame.K_RIGHT, pygame.K_d]
K_UP = [pygame.K_UP, pygame.K_w]
K_DOWN = [pygame.K_DOWN, pygame.K_s]
K_DROP_ITEM = pygame.K_z
K_GRUNT = pygame.K_g

RUN_KEYS = [pygame.K_LSHIFT, pygame.K_RSHIFT]

K_USE = pygame.K_e  # Use Inventory item
K_TOGGLE_EDIT_MODE = pygame.K_F1
K_NEXT_LAYER = pygame.K_t
K_SAVE_LEVEL = pygame.K_F5
K_CHANGE_BLOCK_UP = pygame.K_PAGEUP
K_CHANGE_BLOCK_DOWN = pygame.K_PAGEDOWN
MOVEMENT_KEYS = K_UP + K_DOWN + K_LEFT + K_RIGHT

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
