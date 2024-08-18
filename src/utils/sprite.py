""" Sprite utilities """

import random

import PIL
import arcade
from PIL.Image import Resampling
from arcade import TileMap, Texture, TextureAnimationSprite, TextureKeyframe, TextureAnimation
from arcade.resources import resolve_resource_path, resolve


def tilemap_size(tilemap: TileMap) -> tuple:
    """

    Calculate pixel size of a tilemap
    @param tilemap: The tile map

    @return: (width, height)
    """
    width = tilemap.width * tilemap.tile_width
    height = tilemap.height * tilemap.tile_height
    return width, height


def random_position(tilemap: TileMap) -> tuple:
    """
    Get a random position on a tilemap
    @param tilemap: The tile map
    @return: (x, y)
    """
    width, height = tilemap_size(tilemap)

    rand_x = random.randint(0, width)
    rand_y = random.randint(0, height)

    return rand_x, rand_y


def load_animated_gif(resource_name, size) -> TextureAnimationSprite:
    """
    Attempt to load an animated GIF as an :class:`TextureAnimationSprite`.

    .. note::

        Many older GIFs will load with incorrect transparency for every
        frame but the first. Until the Pillow library handles the quirks of
        the format better, loading animated GIFs will be pretty buggy. A
        good workaround is loading GIFs in another program and exporting them
        as PNGs, either as sprite sheets or a frame per file.
    """

    file_name = resolve(resource_name)
    image_object = PIL.Image.open(file_name)
    if not image_object.is_animated:
        raise TypeError(f"The file {resource_name} is not an animated gif.")

    sprite = TextureAnimationSprite()
    keyframes = []
    for frame in range(image_object.n_frames):
        image_object.seek(frame)
        frame_duration = image_object.info["duration"]
        image = image_object.convert("RGBA")
        image = image.resize(
            size,
            resample=Resampling.BILINEAR
        )
        texture = Texture(image)
        texture.file_path = file_name
        # sprite.textures.append(texture)
        keyframes.append(TextureKeyframe(texture, frame_duration))

    animation = TextureAnimation(keyframes=keyframes)
    sprite.animation = animation
    return sprite
