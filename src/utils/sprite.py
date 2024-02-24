import arcade
from arcade import Point

DISTANCE = 5
def get_closest_sprite(player_sprite, sprite_list, tolerance = DISTANCE):

    pos_x, pos_y = player_sprite.center_x, player_sprite.center_y

    check_points = [
        (pos_x + tolerance, pos_y),
        (pos_x - tolerance, pos_y),
        (pos_x, pos_y + tolerance),
        (pos_x, pos_y - tolerance)
    ]

    for point in check_points:
        closest = arcade.get_sprites_at_point(point, sprite_list)
        print(closest)

    return None
