import arcade.sprite
from utils.postprocessing.fog import Fog
from utils.postprocessing.colortint import ColorTint


class PostProcessing:
    def __init__(self):
        self.pipeline = []

    def setup(self, args):
        self.pipeline = []

        self.pipeline.append(
            ColorTint().setup(args)
        )

        return self

    def update(self, delta_time, args) -> None:
        for effect in self.pipeline:
            effect.update(delta_time, args)

    def draw(self) -> None:
        """ Draw all postprocessing effects """

        for effect in self.pipeline:
            effect.draw()
