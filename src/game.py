#!/usr/bin/env python

"""
    Game main class
    Initialized the base of the game
"""
import os
import pygame
import constants.game
from pygame.locals import QUIT
import time
import utils.audio
from utils.fps_counter import FPSCounter
import components.menu

class Game:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = None
        self.fps_counter = FPSCounter()
        self.running = True
        self.clock = pygame.time.Clock()
        self.resource_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.current_component = None
        self.fullscreen = constants.game.FULLSCREEN

        self.monotype_font = pygame.font.Font(
            os.path.join(
                self.resource_dir,
                'fonts',
                constants.game.MONOTYPE_FONT),
            constants.game.DEBUG_OUTPUT_FONT_SIZE)
      
    def start(self):
        self.init_screen()

        self.current_component = components.menu.Menu(self.resource_dir)

        self.main_loop()

    def init_screen(self):
        flags = pygame.SCALED

        if self.fullscreen:
            flags = flags | pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(
            [
                constants.game.SCREEN_WIDTH,
                constants.game.SCREEN_HEIGHT
            ],
            flags,
            vsync=int(
                constants.game.VSYNC
                )
            )

        pygame.display.set_caption(constants.game.WINDOW_CAPTION)

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

        self.init_screen()

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update_screen()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    self.screenshot()
                if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    self.toggle_fullscreen()
                
        if self.current_component:
            self.current_component.handle_events()

    def screenshot(self):
        # TODO store in home dir

        screenshot_dir = os.path.join(self.resource_dir, 'screenshots')

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        screenshot_file = os.path.join(
            screenshot_dir,
            time.strftime("%Y%m%d-%H%M%S") + '.jpg'
            )

        pygame.image.save(self.screen, screenshot_file)
        camera_sound = os.path.join(self.resource_dir, 'sounds', 'screenshot.ogg')
        utils.audio.play_sound(camera_sound)

    def update_screen(self):
        # Filling the window with black color
        self.screen.fill((0, 0, 0))

        self.clock.tick(constants.game.FPS_LIMIT)

        if self.current_component:
            self.current_component.update_screen(self.screen)

        if constants.game.SHOW_FPS:
            self.show_fps()

        # Updating the display surface
        # pygame.display.update()
        pygame.display.flip()


    # Create Text
    def render_text(self, what, color, where):
        text = self.monotype_font.render(what, 1, pygame.Color(color))
        self.screen.blit(text, where)

    def show_fps(self):
        self.fps_counter.get_fps(self.clock)
        self.render_text(self.fps_counter.get_fps_text(),
                         (255, 255, 255), (10, 10))


game = Game()
game.start()
