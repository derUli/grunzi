import pygame
import os
import pygame_menu
import constants.game
from utils.fps_counter import FPSCounter
from components.component import Component

class MainGame(Component):
    def __init__(self, data_dir, handle_change_component):
        self.screen = None