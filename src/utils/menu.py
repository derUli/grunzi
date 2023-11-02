import pygame_menu


def make_menu(title, screen):
    return pygame_menu.Menu(
        height=screen.get_height() / 2,
        theme=pygame_menu.themes.THEME_BLUE,
        title=title,
        width=screen.get_width() / 3)
