from typing import Self

import arcade

from state.argscontainer import ArgsContainer
from utils.postprocessing.effect import Effect

COLOR_GREEN = (124, 252, 0)
COLOR_YELLOW = (252, 234, 2)
COLOR_WHITE = (228, 227, 225)

INDEX_YELLOW = 0
INDEX_GREEN = 1
INDEX_WHITE = 2


class ColorTint(Effect):
    def setup(self, args: ArgsContainer) -> Self:
        """
        Setup fog effect
        @param args: ArgsContainer
        @return: Self
        """

        self.spritelist.clear()

        w, h = arcade.get_window().get_size()

        sprite = arcade.sprite.SpriteSolidColor(w, h, color=COLOR_YELLOW)
        sprite.alpha = 0
        self.spritelist.append(sprite)

        sprite = arcade.sprite.SpriteSolidColor(w, h, color=COLOR_GREEN)
        sprite.alpha = 0
        self.spritelist.append(sprite)

        sprite = arcade.sprite.SpriteSolidColor(w, h, color=COLOR_WHITE)
        sprite.alpha = 0
        self.spritelist.append(sprite)

        return self

    def update(self, delta_time: float, args: ArgsContainer) -> None:

        w, h = arcade.get_window().get_size()
        from constants.layers import LAYER_SUN
        from sprites.decoration.sun import Sun
        self.update_it(
            args=args,
            index=INDEX_YELLOW,
            layer_name=LAYER_SUN,
            klass=Sun,
            radius=h,
            max_alpha=240
        )

        from constants.layers import LAYER_NPC
        from sprites.bullet.slimerbullet import SlimerBullet
        self.update_it(
            args=args,
            index=INDEX_GREEN,
            layer_name=LAYER_NPC,
            klass=SlimerBullet,
            radius=h,
            max_alpha=100
        )

        from constants.layers import LAYER_MOON
        from sprites.decoration.moon import Moon
        self.update_it(
            args=args,
            index=INDEX_WHITE,
            layer_name=LAYER_MOON,
            klass=Moon,
            radius=h,
            max_alpha=240
        )

    def update_it(self, args, index, layer_name, klass, radius, max_alpha):
        w, h = arcade.get_window().get_size()
        x, y = args.player.position

        if x < w * 0.5:
            x = w * 0.5

        if y < h * 0.5:
            y = h * 0.5

        self.spritelist[index].position = (x, y)

        if layer_name not in args.scene.name_mapping:
            return

        alpha = 0
        one = max_alpha / radius

        found = False

        for sprite in args.scene[layer_name]:
            if isinstance(sprite, klass):
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
            alpha = self.spritelist[index].alpha - 1

            if alpha < 0:
                alpha = 0

        self.spritelist[index].alpha = alpha
