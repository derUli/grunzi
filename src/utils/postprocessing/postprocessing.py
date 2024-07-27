from state.argscontainer import ArgsContainer
from utils.postprocessing.colortint import ColorTint
from utils.postprocessing.filmgrain import FilmGrain
from utils.postprocessing.fog import Fog


class PostProcessing:
    def __init__(self):
        self.pipeline = []

    def setup(self, args: ArgsContainer):
        self.pipeline = []

        if args.state.settings.weather and args.state.difficulty.options['fog']:
            self.pipeline.append(
                Fog().setup(args)
            )

        if args.state.settings.color_tint:
            self.pipeline.append(
                ColorTint().setup(args)
            )

        self.pipeline.append(
            FilmGrain().setup(args)
        )

        return self

    def update(self, delta_time: float, args: ArgsContainer) -> None:
        for effect in self.pipeline:
            effect.update(delta_time, args)

    def draw(self) -> None:
        """ Draw all postprocessing effects """

        for effect in self.pipeline:
            effect.draw()
