import random

import arcade

DISTANCE = 5


def get_closest_sprite(player_sprite, sprite_list, tolerance=DISTANCE):
    pos_x, pos_y = player_sprite.center_x, player_sprite.center_y

    check_points = [
        (pos_x + tolerance, pos_y),
        (pos_x - tolerance, pos_y),
        (pos_x, pos_y + tolerance),
        (pos_x, pos_y - tolerance)
    ]

    for point in check_points:
        closest = arcade.get_sprites_at_point(point, sprite_list)

    return None


def tilemap_size(tilemap):
    width = tilemap.width * tilemap.tile_width
    height = tilemap.height * tilemap.tile_height
    return width, height


def random_position(tilemap):
    width, height = tilemap_size(tilemap)

    rand_x = random.randint(0, width)
    rand_y = random.randint(0, height)

    return rand_x, rand_y
