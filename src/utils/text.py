""" Text utils """

import arcade
from arcade import Color

from constants.fonts import FONT_DEFAULT

MARGIN = 10

MEDIUM_FONT_SIZE = 14

SMALL_FONT_SIZE = 12
INPUT_FONT_SIZE = 22
LARGE_FONT_SIZE = 16
EXTRA_LARGE_FONT_SIZE = 20

HEADLINE_FONT_SIZE = 40
LOGO_FONT_SIZE = 80


def create_text(
        text: str,
        start_x: float = MARGIN,
        start_y: float = MARGIN,
        color: Color = arcade.csscolor.WHITE,
        font_size: int = MEDIUM_FONT_SIZE,
        font_name: str = FONT_DEFAULT,
        anchor_x: str = 'left',
        anchor_y: str = 'bottom',
        align: str = 'left',
        width: int | None = None,
        multiline: bool = False,
        bold: bool = False
) -> arcade.Text:
    """

    @param text: The text
    @param start_x: The position X
    @param start_y: The position Y
    @param color: The text color
    @param font_size: The font size
    @param font_name: The font name
    @param anchor_x: The anchor X
    @param anchor_y: The anchor Y
    @param align: The align
    @param width: The width
    @param multiline: Is multiline
    @param bold: Is bolt
    @return: Text
    """
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
        font_name=font_name,
        bold=bold
    )


def label_value(label: str, value: any) -> str:
    """
    @param label: label text
    @param value: value
    @return: Label Value string
    """
    return ': '.join([label, str(value)])
