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
    title_font_size=30,
    title_font_shadow=True,
    widget_font_color=BOTTOM_UI_BACKGROUND,
    widget_font_size=22
)


def make_menu(title, limit_fps=0):
    THEME_PIG.fps = limit_fps
    return pygame_menu.Menu(
        height=480,
        theme=THEME_PIG,
        title=title,
        width=640
    )
