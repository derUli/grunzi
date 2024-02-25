import random

DISTANCE = 5


def tilemap_size(tilemap):
    width = tilemap.width * tilemap.tile_width
    height = tilemap.height * tilemap.tile_height
    return width, height


def random_position(tilemap):
    width, height = tilemap_size(tilemap)

    rand_x = random.randint(0, width)
    rand_y = random.randint(0, height)

    return rand_x, rand_y
