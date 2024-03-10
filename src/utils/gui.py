import PIL
import arcade
from arcade.gui import UIFlatButton

from constants.fonts import FONT_DEFAULT
from utils.text import MEDIUM_FONT_SIZE


def get_texture_by_value(width, height, value=False):
    red_background = PIL.Image.new("RGBA", (width, height), arcade.csscolor.BLACK)
    green_background = PIL.Image.new("RGBA", (width, height), arcade.csscolor.HOTPINK)

    texture_red = arcade.texture.Texture(name='red_background', image=red_background)
    texture_green = arcade.texture.Texture(name='green_background', image=green_background)

    if value:
        return texture_green

    return texture_red


def get_button_style() -> dict:
    """
    Get the style for the flat button
    @return: Style
    """
    style = UIFlatButton.DEFAULT_STYLE

    for index in style:
        style[index]['font_name'] = FONT_DEFAULT
        style[index]['font_size'] = MEDIUM_FONT_SIZE
    return style
