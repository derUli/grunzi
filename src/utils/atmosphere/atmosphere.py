import pygame
import time
from utils.atmosphere.daynightcycle import DayNightCycle

class Atmosphere:

    def __init__(self):
        self.atmosphere_layers = []
        pass

    def start(self):
        self.reset()

    def reset(self):
        self.atmosphere_layers = [
            DayNightCycle()
        ]

        for layer in self.atmosphere_layers:
            layer.reset()

    def draw(self, screen):
        for layer in self.atmosphere_layers:
            layer.draw(screen)
       