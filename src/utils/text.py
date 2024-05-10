""" Text utils """

import arcade

from constants.fonts import FONT_DEFAULT

MARGIN = 10

MEDIUM_FONT_SIZE = 14

HEADLINE_FONT_SIZE = 40
LOGO_FONT_SIZE = 80


def create_text(
        text,
        start_x=MARGIN,
        start_y=MARGIN,
        color=arcade.csscolor.WHITE,
        font_size=MEDIUM_FONT_SIZE,
        font_name=FONT_DEFAULT,
        anchor_x='left',
        anchor_y='bottom',
        align='left',
        width=None,
        multiline=False,
        bold=False
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
        font_name=font_name,
        bold=bold
    )


def label_value(label: str, value: any) -> str:
    """
    @param label: label text
    @param value: value
    @return:
    """
    return ': '.join([label, str(value)])
