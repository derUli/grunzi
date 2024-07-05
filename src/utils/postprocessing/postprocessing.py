import os

import arcade

from utils.postprocessing.colortint import ColorTint
from utils.postprocessing.fog import Fog
from utils.sprite import load_animated_gif


class PostProcessing:
    def __init__(self):
        self.pipeline = []

    def setup(self, args):
        self.pipeline = []

        if args.state.difficulty.options['fog']:
            self.pipeline.append(
                Fog().setup(args)
            )

        self.pipeline.append(
            ColorTint().setup(args)
        )

        w, h = arcade.get_window().get_size()
        self.filmgrain = load_animated_gif(
            os.path.join(args.state.animation_dir, 'grain.gif'),
            (w, h)
        )
        self.filmgrain.alpha = 20 * 0.5
        self.filmgrain.position = args.player.position

        return self

    def update(self, delta_time, args) -> None:
        for effect in self.pipeline:
            effect.update(delta_time, args)

        w, h = arcade.get_window().get_size()

        self.filmgrain.position = args.player.position
        self.filmgrain.center_x = max(w * 0.5, self.filmgrain.center_x)
        self.filmgrain.center_y = max(h * 0.5, self.filmgrain.center_y)
        self.filmgrain.update_animation(delta_time)


    def draw(self) -> None:
        """ Draw all postprocessing effects """

        for effect in self.pipeline:
            effect.draw()

        self.filmgrain.draw()