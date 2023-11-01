#!/usr/bin/env python

"""
    Game main class
    Initialized the base of the game
"""
import os
import pygame
import constants.game
import constants.headup
import constants.sound
from pygame.locals import QUIT
import time
import utils.audio
from utils.fps_counter import FPSCounter
import components.menu
import signal

class Game:

    def __init__(self):
        pygame.init()

        self.screen = None
        self.fps_counter = FPSCounter()
        self.running = True
        self.clock = pygame.time.Clock()
        self.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.current_component = None
        self.fullscreen = constants.game.FULLSCREEN
      
    def start(self):
        self.init_screen()
        self.change_component(components.menu.Menu)
        
        signal.signal(signal.SIGINT, self.quit)
        signal.signal(signal.SIGTERM, self.quit)
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

        if self.current_component:
            self.current_component.set_screen(self.screen)

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
                self.quit()
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    self.screenshot()
                if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    self.toggle_fullscreen()
                
            self.current_component.handle_event(event)

    def quit(self, sig = None, frame = None):
        self.running = False

    def screenshot(self):
        # TODO store in home dir

        screenshot_dir = os.path.join(self.data_dir, 'screenshots')

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        screenshot_file = os.path.join(
            screenshot_dir,
            time.strftime("%Y%m%d-%H%M%S") + '.jpg'
            )

        pygame.image.save(self.screen, screenshot_file)
        camera_sound = os.path.join(self.data_dir, 'sounds', 'screenshot.ogg')
        utils.audio.play_sound(camera_sound)

    def update_screen(self):
        # Filling the window with black color
        self.screen.fill((0, 0, 0))

        self.clock.tick(constants.game.FPS_LIMIT)

        self.current_component.update_screen(self.screen)

        if constants.game.SHOW_FPS:
            self.show_fps()

        # Updating the display surface
        # pygame.display.update()
        pygame.display.flip()


    def show_fps(self):
        self.fps_counter.get_fps(self.clock)
        self.current_component.render_text(self.fps_counter.get_fps_text(),
                         (0, 247, 0), constants.headup.FPS_TEXT_POSITION)


    def change_component(self, component):        
        if self.current_component:
            self.current_component.unmount()


        self.current_component = component(self.data_dir, self.change_component)

        if self.current_component:
            self.current_component.set_screen(self.screen)
            
        self.current_component.mount()

game = Game()
game.start()
