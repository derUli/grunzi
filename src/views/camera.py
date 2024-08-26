""" Center camera to player """


def center_camera_to_player(player_sprite, camera, size: tuple) -> None:
    """
    Center camera to play
    @param player_sprite: The player
    @param camera: The camera
    @param size: The size of the tilemap
    """
    # Find where player is, then calculate lower left corner from that
    screen_center_x = player_sprite.center_x - (camera.viewport_width / 2)
    screen_center_y = player_sprite.center_y - (camera.viewport_height / 2)

    # Set some limits on how far we scroll
    screen_center_x = max(screen_center_x, 0)
    screen_center_y = max(screen_center_y, 0)

    w, h = size
    screen_center_x = min(screen_center_x, w)
    screen_center_y = min(screen_center_y, h)

    # Here's our center, move to it
    player_centered = screen_center_x, screen_center_y
    camera.move_to(player_centered)

