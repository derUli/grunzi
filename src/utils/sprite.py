""" Sprite utilities """

import random

import PIL
from PIL.Image import Resampling
from arcade import TileMap, AnimatedTimeBasedSprite, Texture, AnimationKeyframe
from arcade.resources import resolve_resource_path


def tilemap_size(tilemap: TileMap) -> tuple:
    """

    Calculate pixel size of a tilemap
    @param tilemap: The tile map

    @return: (width, height)
    """
    width = tilemap.width * tilemap.tile_width
    height = tilemap.height * tilemap.tile_height
    return width, height


def random_position(tilemap: TileMap = None, map_size=None) -> tuple:
    """
    Get a random position on a tilemap
    @param tilemap: The tile map
    @return: (x, y)
    """
    if tilemap:
        width, height = tilemap_size(tilemap)
    else:
        width, height = map_size

    rand_x = random.randint(0, width)
    rand_y = random.randint(0, height)

    return rand_x, rand_y


def load_animated_gif(resource_name, size, resample=Resampling.BILINEAR) -> AnimatedTimeBasedSprite:
    """
    Attempt to load an animated GIF as an :class:`AnimatedTimeBasedSprite`.

    Many older GIFs will load with incorrect transparency for every
    frame but the first. Until the Pillow library handles the quirks of
    the format better, loading animated GIFs will be pretty buggy. A
    good workaround is loading GIFs in another program and exporting them
    as PNGs, either as sprite sheets or a frame per file.
    """

    file_name = resolve_resource_path(resource_name)
    # print(file_name)
    image_object = PIL.Image.open(file_name)
    if not image_object.is_animated:
        raise TypeError(f"The file {resource_name} is not an animated gif.")

    sprite = AnimatedTimeBasedSprite()
    for frame in range(image_object.n_frames):
        image_object.seek(frame)
        frame_duration = image_object.info['duration']
        image = image_object.convert("RGBA")

        image = image.resize(
            size,
            resample=resample
        )

        texture = Texture(f"{resource_name}-{frame}", image)
        sprite.textures.append(texture)
        sprite.frames.append(AnimationKeyframe(0, frame_duration, texture))

    sprite.texture = sprite.textures[0]
    return sprite
