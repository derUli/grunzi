import os

import arcade

from state.argscontainer import ArgsContainer
from utils.postprocessing.effect import Effect
from utils.sprite import load_animated_gif

COLOR_GREEN = (124, 252, 0)
COLOR_YELLOW = (252, 234, 2)
COLOR_WHITE = (228, 227, 225)

INDEX_YELLOW = 0
INDEX_GREEN = 1
INDEX_WHITE = 2


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
            (w, h)
        )

        filmgrain.alpha = 20 * args.state.settings.filmgrain
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

        self.filmgrain.alpha = 20 * args.state.settings.filmgrain

        if self.filmgrain.alpha <= 0:
            return

        w, h = arcade.get_window().get_size()

        self.filmgrain.position = args.player.position
        self.filmgrain.center_x = max(w * 0.5, self.filmgrain.center_x)
        self.filmgrain.center_y = max(h * 0.5, self.filmgrain.center_y)

        self.filmgrain.update_animation(1/4)
