import os
import pygame
import time
from pygame.locals import *

class Test:

    def __init__(self):
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = None
        self.fps_limit = 0
        self.fps = None
        self.max_fps = None
        self.min_fps = None
        self.fps_avg = []
        self.caption = 'My Game'
        self.running = True
        self.clock = pygame.time.Clock()
        
        self.root_dir = os.path.dirname(__file__)
        self.monotype_font = pygame.font.Font(os.path.join(self.root_dir, 'monotype.ttf'), 12)
        self.skybox_image = None
        self.skybox_positions = []

        self.last_fps_shown = int(time.time())

        
    def start(self):
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height], pygame.FULLSCREEN, vsync=1)
        
        pygame.display.set_caption(self.caption)
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
        
        self.clock.tick(self.fps_limit)
        self.show_fps()
        # Updating the display surface
        pygame.display.update()


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

    #Create Text
    def render_text(self, what, color, where):
        text = self.monotype_font.render(what, 1, pygame.Color(color))
        self.screen.blit(text, where)

    def avg_fps(self):
        return int(sum(self.fps_avg) / len(self.fps_avg))


    def show_fps(self):
        fps = self.get_fps()


        text = str(self.fps) + ' (AVG: ' + str(self.avg_fps()) + ', MIN: ' + str(self.min_fps) + ', MAX: ' + str(self.max_fps) + ')'
        self.render_text(text, (255,255,255), (10, 10))

    def get_fps(self):
        fps = int(self.clock.get_fps())

        
        if not self.fps:
            self.fps = fps
            self.fps_avg.append(self.fps)
        
        if not self.max_fps:
            self.max_fps = fps

        if not self.min_fps and fps > 0:
            self.min_fps = fps
        
        if fps > self.max_fps:
            self.max_fps = fps

        if self.min_fps != None and fps < self.min_fps:
            self.min_fps = fps
            

        if int(time.time()) > self.last_fps_shown:
            self.last_fps_shown = int(time.time())
            self.fps = fps
            self.fps_avg.append(fps)

        return fps


game = Test()
game.start()