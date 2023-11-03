import pygame_menu


def make_menu(title, screen):
    return pygame_menu.Menu(
        height=337,
        theme=pygame_menu.themes.THEME_BLUE,
        title=title,
        width=600
        )
