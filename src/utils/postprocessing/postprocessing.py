import arcade.sprite
from utils.postprocessing.fog import Fog
from utils.postprocessing.lighting import Lighting


class PostProcessing:
    def __init__(self):
        self.pipeline = []
        self.sprite = None

    def setup(self, args):
        self.pipeline = []
        if args.state.difficulty.options['fog']:
            self.pipeline.append(
                Fog().setup(args)
            )

        self.pipeline.append(
            Lighting().setup(args)
        )

        return self

    def update(self, delta_time, args) -> None:
        for effect in self.pipeline:
            effect.update(delta_time, args)

    def draw(self) -> None:
        """ Draw all postprocessing effects """

        for effect in self.pipeline:
            effect.draw()

        if self.sprite:
            self.sprite.draw()
