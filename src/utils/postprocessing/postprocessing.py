class PostProcessing:
    def __init__(self):
        self.pipeline = []

    def setup(self, args):
        self.pipeline = []
        return self

    def update(self, delta_time, args):
        for effect in self.pipeline:
            effect.update(delta_time, args)

    def draw(self):
        for effect in self.pipeline:
            effect.draw()