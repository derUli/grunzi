""" Menu stuff """
import pygame_menu

from constants.headup import BOTTOM_UI_BACKGROUND, PIGGY_PINK

THEME_PIG = pygame_menu.Theme(
    background_color=PIGGY_PINK,
    scrollbar_shadow=True,
    widget_cursor=None,
    scrollbar_cursor=None,
    scrollbar_slider_color=BOTTOM_UI_BACKGROUND,
    scrollbar_slider_hover_color=BOTTOM_UI_BACKGROUND,
    scrollbar_slider_pad=2,
    selection_color=BOTTOM_UI_BACKGROUND,
    title_background_color=BOTTOM_UI_BACKGROUND,
    title_font_color=(228, 230, 246),
    title_font_size=26,
    title_font_shadow=False,
    title_font_antialias=True,
    widget_font_antialias=True,
    widget_font_color=BOTTOM_UI_BACKGROUND,
    widget_font_size=20,
)

WIDTH = 640
HEIGHT = 480


def make_menu(title: str, limit_fps: int = 0) -> pygame_menu.Menu:
    """ Make pygame menu """
    THEME_PIG.fps = limit_fps
    return pygame_menu.Menu(
        width=WIDTH,
        height=HEIGHT,
        theme=THEME_PIG,
        title=title
    )


def get_longest_option(options: list) -> str:
    """ Get the longest option """
    longest = ''

    for text, value in options:
        if len(text) > len(longest):
            longest = text

    return longest
