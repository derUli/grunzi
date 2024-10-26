import os

import arcade

from state.argscontainer import ArgsContainer
from utils.postprocessing.effect import Effect
from utils.sprite import load_animated_gif

ALPHA = 18


class FilmGrain(Effect):
    def setup(self, args: ArgsContainer):
        """
        Setup fog effect
        @param args: ArgsContainer
        @return: Self
        """

        self.spritelist.clear()

        w, h = arcade.get_window().get_size()
        filmgrain = load_animated_gif(
            os.path.join(args.state.animation_dir, 'grain.gif'),
            (w, h),
            resample=args.state.settings.pil_resample
        )

        filmgrain.alpha = ALPHA * args.state.settings.filmgrain
        filmgrain.position = args.player.position
        self.spritelist.append(filmgrain)

        return self

    @property
    def filmgrain(self):
        if any(self.spritelist):
            return self.spritelist[0]

        return None

    def update(self, delta_time: float, args: ArgsContainer) -> None:
        if not self.filmgrain:
            return

        self.filmgrain.alpha = ALPHA * args.state.settings.filmgrain

        if self.filmgrain.alpha <= 0:
            return

        w, h = arcade.get_window().get_size()

        self.filmgrain.position = args.player.position
        self.filmgrain.center_x = max(w * 0.5, self.filmgrain.center_x)
        self.filmgrain.center_y = max(h * 0.5, self.filmgrain.center_y)

        self.filmgrain.update_animation(1 / 4)
