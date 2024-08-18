""" Text utils """

import arcade
from arcade.color import Color

from constants.fonts import FONT_DEFAULT

MARGIN = 10

FONT_SIZE_MEDIUM = 14
FONT_SIZE_SMALL = 12
FONT_SIZE_INPUT = 22
FONT_SIZE_LARGE = 16
FONT_SIZE_EXTRA_LARGE = 20
FONT_SIZE_HEADLINE = 40
FONT_SIZE_LOGO = 80


def create_text(
        text: str,
        x: float = MARGIN,
        y: float = MARGIN,
        color: Color = arcade.csscolor.WHITE,
        font_size: int = FONT_SIZE_MEDIUM,
        font_name: str = FONT_DEFAULT,
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
        color=color,
        font_size=font_size,
        align=align,
        x=x,
        y=y,
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
