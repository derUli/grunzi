""" Center camera to player """
import arcade

def center_camera_to_player(player_sprite, camera: arcade.Camera) -> None:
    camera.center(player_sprite.position)
