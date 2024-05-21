from utils.postprocessing.fog import Fog


class PostProcessing:
    def __init__(self):
        self.pipeline = []

    def setup(self, args):
        self.pipeline = []
        if args.state.difficulty.options['fog']:
            self.pipeline.append(
                Fog().setup(args)
            )

        return self

    def update(self, delta_time, args):
        for effect in self.pipeline:
            effect.update(delta_time, args)

    def draw(self):
        for effect in self.pipeline:
            effect.draw()
