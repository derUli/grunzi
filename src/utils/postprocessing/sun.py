import arcade

from constants.layers import LAYER_SUN
from utils.postprocessing.effect import Effect

COLOR_SUN = (254, 222, 23, 255)
class Sun(Effect):

    def __init__(self):
        super().__init__()

    def setup(self, args):

        self.spritelist.clear()
        w, h = arcade.get_window().get_size()

        sprite = arcade.sprite.SpriteSolidColor(w, h, color=COLOR_SUN)

        sprite.center_x = w / 2
        sprite.center_y = h / 2

        sprite.alpha = 0

        self.spritelist.append(sprite)
        return self

    def update(self, delta_time, args):
        if LAYER_SUN not in args.scene:
            return

        w, h = arcade.get_window().get_size()
        sun = args.scene[LAYER_SUN][0]

        difference = arcade.get_distance_between_sprites(sun, args.player)

        alpha = (h / difference) * 100

        if alpha < 0:
            alpha = 0

        if alpha > 255:
            alpha = 255

        self.spritelist[0].alpha = alpha

    def draw(self):
        if self.spritelist[0].alpha <= 0:
            return

        self.spritelist.draw()
