""" Center camera to player """
import arcade


def center_camera_to_player(player_sprite, camera: arcade.Camera, size: tuple) -> None:
    camera.center(player_sprite.position)
