import pygame
import os

class Menu:

    def __init__(self, resource_dir):
        self.skybox_positions = []
        self.skybox_image = pygame.image.load(
            os.path.join(resource_dir, 'images', 'menu', 'sky.jpg')).convert()
        self.skybox_positions = [
            (0.0, 0.0),
            (float(self.skybox_image.get_width()), 0.0),
        ]

    def update_screen(self, screen):
        self.update_skybox(screen)
    
    def handle_events(self):
        return 

    def update_skybox(self, screen):
        i = 0

        for skybox in self.skybox_positions:
            screen.blit(self.skybox_image, skybox)

            x, y = skybox

            if x < self.skybox_image.get_width() * -1.0:
                x = float(self.skybox_image.get_width())

            x -= 0.1

            self.skybox_positions[i] = (x, y)
            i += 1