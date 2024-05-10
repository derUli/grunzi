""" Sun """
from arcade import Scene, Camera

from sprites.sprite import Sprite
from utils.scene import get_layer

MARGIN_RIGHT = 20


class Sun(Sprite):
    """ Sun """

    def update_sun(self, camera: Camera):
        """ Update sun position """
        camera_x, camera_y = camera.position
        x, y, viewport_w, viewport_h = camera.viewport

        self.left = camera_x + viewport_w - self.width - MARGIN_RIGHT


def update_sun(scene: Scene, camera_sprites: Camera):
    """ Update sun """
    from constants.layers import LAYER_SUN

    for sprite in get_layer(LAYER_SUN, scene):
        sprite.update_sun(camera_sprites)
