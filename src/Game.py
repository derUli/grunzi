#!/usr/bin/env python

import os
import pygame
import time
from utils.FPSCounter import FPSCounter
import constants.game
from pygame.locals import QUIT

"""
    Game main class
    Initialized the base of the game
"""
class Game:

    def __init__(self):
        pygame.init()
        self.screen = None
        self.fps_counter = FPSCounter()
        self.running = True
        self.clock = pygame.time.Clock()

        self.root_dir = os.path.dirname(__file__)
        self.monotype_font = pygame.font.Font(os.path.join(self.root_dir, constants.game.MONOTYPE_FONT), constants.game.DEBUG_OUTPUT_FONT_SIZE)
        self.skybox_image = None
        self.skybox_positions = []

        
    def start(self):
        self.screen = pygame.display.set_mode([constants.game.SCREEN_WIDTH, constants.game.SCREEN_HEIGHT], pygame.FULLSCREEN, vsync=int(constants.game.VSYNC))
        
        pygame.display.set_caption(constants.game.WINDOW_CAPTION)
        self.skybox_image = pygame.image.load(os.path.join(self.root_dir, 'sky.jpg')).convert()

        self.skybox_positions = [
            (0.0, 0.0),
            (float(self.skybox_image.get_width()), 0.0),
        ]

        self.main_loop()


    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update_screen()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False


    def update_screen(self):
        # Filling the window with black color
        self.screen.fill((0, 0, 0))
        self.update_skybox()
        
        self.clock.tick(constants.game.FPS_LIMIT)
        self.show_fps()
        # Updating the display surface
        pygame.display.update()
        pygame.display.flip()


    def update_skybox(self):
        i = 0

        for skybox in self.skybox_positions:
            self.screen.blit(self.skybox_image, skybox)

            x, y = skybox

            if x < self.skybox_image.get_width() * -1.0:
                x = float(self.skybox_image.get_width())

            x -= 0.1
            
            self.skybox_positions[i] = (x, y)

            i+=1

    # Create Text
    def render_text(self, what, color, where):
        text = self.monotype_font.render(what, 1, pygame.Color(color))
        self.screen.blit(text, where)

    def show_fps(self):
        self.fps_counter.get_fps(self.clock)
        self.render_text(self.fps_counter.get_fps_text(), (255,255,255), (10, 10))


game = Game()
game.start()