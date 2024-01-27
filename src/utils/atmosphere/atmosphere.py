from utils.atmosphere.daynightcycle import DayNightCycle
from utils.atmosphere.fog import Fog
from utils.atmosphere.rain import Rain


class Atmosphere:

    def __init__(self, sprites_dir, image_cache):
        self.layers = []
        self.sprites_dir = sprites_dir
        self.image_cache = image_cache

    def start(self, args={}):
        self.reset()

        for layer in self.layers:
            layer.start(args, self.sprites_dir, self.image_cache)

    def reset(self):
        self.layers = [
            Fog(),
            Rain()
        ]

        for layer in self.layers:
            layer.reset()

    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)

    def to_dict(self):
        savdict = {}

        for layer in self.layers:
            savdict = savdict | layer.to_dict()

        return savdict

    def get_layer_by_id(self, id):
        for layer in self.layers:
            if layer.id == id:
                return layer

        return None
