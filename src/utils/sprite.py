""" Sprite utilities """

import random

from arcade import TileMap

DISTANCE = 5


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
