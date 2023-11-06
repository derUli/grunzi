import pygame
from pygame_emojis import load_emoji

CURSOR_SIZE = (32, 32)


def default_cursor():
    surf = load_emoji('🐽')
    return pygame.cursors.Cursor(CURSOR_SIZE, surf)
