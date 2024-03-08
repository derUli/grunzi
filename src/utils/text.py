import arcade
from arcade.gui import UIFlatButton

from constants.fonts import DEFAULT_FONT

MARGIN = 10
DEBUG_COLOR = arcade.csscolor.GHOST_WHITE

MEDIUM_FONT_SIZE = 14
LARGE_FONT_SIZE = 16
LOGO_FONT_SIZE = 80

DEBUG_FONT_SIZE = 12


def create_text(
        text,
        start_x=MARGIN,
        start_y=MARGIN,
        color=arcade.csscolor.WHITE,
        font_size=MEDIUM_FONT_SIZE,
        font_name=DEFAULT_FONT,
        anchor_x='left',
        anchor_y='bottom',
        align='left',
        width=None,
        multiline=False
):
    return arcade.Text(
        text=text,
        start_x=start_x,
        start_y=start_y,
        color=color,
        font_size=font_size,
        align=align,
        anchor_x=anchor_x,
        anchor_y=anchor_y,
        width=width,
        multiline=multiline,
        font_name=font_name
    )


def get_style():
    style = UIFlatButton.DEFAULT_STYLE
    for index in style:
        style[index]['font_name'] = DEFAULT_FONT
        style[index]['font_size'] = MEDIUM_FONT_SIZE
    return style


def label_value(label: str, value: any) -> str:
    """
    @param label: label text
    @param value: value
    @return:
    """
    return ': '.join([label, str(value)])
