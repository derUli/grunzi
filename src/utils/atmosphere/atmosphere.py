import pygame
import time
from utils.atmosphere.daynightcycle import DayNightCycle
from utils.atmosphere.fog import Fog
from utils.atmosphere.rain import Rain


class Atmosphere:

    def __init__(self):
        self.atmosphere_layers = []
        pass

    def start(self, args = {}):
        self.reset()

        for layer in self.atmosphere_layers:
            layer.start(args)

    def reset(self):
        self.atmosphere_layers = [
            Fog(),
            Rain(),
            DayNightCycle()
        ]

        for layer in self.atmosphere_layers:
            layer.reset()

    def draw(self, screen):
        for layer in self.atmosphere_layers:
            layer.draw(screen)
       

    def to_dict(self):
        savdict = {}

        for layer in self.atmosphere_layers:
            savdict = savdict |  layer.to_dict()


        return savdict