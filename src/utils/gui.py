import PIL
import arcade


def get_texture_by_value(width, height, value=False):
    red_background = PIL.Image.new("RGBA", (width, height), arcade.csscolor.BLACK)
    green_background = PIL.Image.new("RGBA", (width, height), arcade.csscolor.HOTPINK)

    texture_red = arcade.texture.Texture(name='red_background', image=red_background)
    texture_green = arcade.texture.Texture(name='green_background', image=green_background)

    if value:
        return texture_green

    return texture_red
