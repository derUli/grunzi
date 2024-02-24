import os.path

import arcade

MARGIN = 10


def create_text(
        text,
        start_x=MARGIN,
        start_y=MARGIN,
        color=arcade.csscolor.WHITE,
        font_size=14,
        anchor_x='left',
        anchor_y='bottom',
        align='left',
        width=None
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
        width=width
    )


def draw_build_number(build_file, window):
    display_text = _('Unknown build')

    if os.path.isfile(build_file):
        with open(build_file, 'r') as f:
            display_text = f.read()

    create_text(display_text, width=window.width - (MARGIN * 2), align='right').draw()


def draw_coins(coins):
    display_text = str(coins).rjust(2, ' ') + ' €'

    create_text(display_text, color=arcade.csscolor.YELLOW).draw()
