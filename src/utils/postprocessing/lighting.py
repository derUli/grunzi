from typing import Self

import arcade

from state.argscontainer import ArgsContainer
from utils.postprocessing.effect import Effect


COLOR_GREEN = (124, 252, 0, 255)

class Lighting(Effect):
    def setup(self, args: ArgsContainer) -> Self:
        """
        Setup fog effect
        @param args: ArgsContainer
        @return: Self
        """

        self.spritelist.clear()

        w, h = arcade.get_window().get_size()

        sprite = arcade.sprite.SpriteSolidColor(w, h, color=COLOR_GREEN)
        sprite.alpha = 0
        self.spritelist.append(sprite)

        return self

    def update(self, delta_time: float, args: ArgsContainer) -> None:
        self.update_green(args)

    def update_green(self, args: ArgsContainer):
        w, h = arcade.get_window().get_size()
        x, y = args.player.position

        if x < w * 0.5:
            x = w * 0.5

        if y < h * 0.5:
            y = h * 0.5

        self.spritelist[0].position = (x, y)

        import sprites.bullet.slimerbullet
        from constants.layers import LAYER_NPC

        if LAYER_NPC not in args.scene.name_mapping:
            return

        alpha = 0
        radius = h
        max_alpha = 100
        one = max_alpha / radius

        found = False

        for sprite in args.scene[LAYER_NPC]:
            if isinstance(sprite, sprites.bullet.slimerbullet.SlimerBullet):
                distance = arcade.get_distance_between_sprites(sprite, args.player)

                if distance > radius:
                    continue

                found = True

                new_alpha = max_alpha - (one * distance)
                if new_alpha > alpha:
                    alpha = new_alpha

        if alpha > max_alpha:
            alpha = max_alpha

        if not found:
            alpha = self.spritelist[0].alpha - 1

            if alpha < 0:
                alpha = 0

        self.spritelist[0].alpha = alpha

    def draw(self) -> None:
        """ Draw fog """

        self.spritelist.draw()
