import os.path

import arcade

MARGIN = 10
DEBUG_COLOR = arcade.csscolor.GHOST_WHITE


def create_text(
        text,
        start_x=MARGIN,
        start_y=MARGIN,
        color=arcade.csscolor.WHITE,
        font_size=14,
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
        multiline=multiline
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


def label_value(label: str, value: any) -> str:
    """
    @param label: label text
    @param value: value
    @return:
    """
    return ': '.join([label, str(value)])

def draw_debug(player_sprite, window):
    debug_lines = []

    debug_lines.append(label_value('POS', str(int(player_sprite.center_x)) + ' ' + str(int(player_sprite.center_y))))
    debug_lines.append(label_value('FPS', str(int(arcade.get_fps()))))

    create_text(
        "\n".join(debug_lines),
        width=window.width - (MARGIN * 2),
        align='right',
        color=DEBUG_COLOR,
        multiline=True
    ).draw()
