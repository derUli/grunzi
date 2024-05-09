from sprites.sprite import Sprite

MARGIN_RIGHT = 20

class Sun(Sprite):
    def update_sun(self, camera):
        camera_x, camera_y = camera.position
        x, y, viewport_w, viewport_h = camera.viewport

        self.left = camera_x + viewport_w - self.width - MARGIN_RIGHT
