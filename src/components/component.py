import pygame
import os
import constants.game
import constants.headup
import utils.audio
import utils.image
import components.menu


class Component(object):
    def __init__(self, data_dir, handle_change_component):
        self.data_dir = data_dir
        self.handle_change_component = handle_change_component
        self.image_cache = utils.image.ImageCache()

        self.monotype_font = pygame.font.Font(
            os.path.join(
                data_dir,
                'fonts',
                constants.game.MONOTYPE_FONT),
            constants.game.DEBUG_OUTPUT_FONT_SIZE
            )

        self.skybox_image = pygame.image.load(
           os.path.join(data_dir, 'images', 'menu', 'sky.jpg')).convert()


        self.skybox_positions = [
            (0.0, 0.0),
            (float(self.skybox_image.get_width()), 0.0),
        ]

    # Create Text
    def render_text(self, what, color, where):
        text = self.monotype_font.render(what, 1, pygame.Color(color))
        self.screen.blit(text, where)
    
    def update_screen(self, screen):
        screen.fill((0,0,0))

    def handle_event(self, event):
        return

    def set_screen(self, screen):
        self.screen = screen

    def mount(self):
        return

    def play_music(self, file):
        file = os.path.join(self.data_dir, 'music', file)
        utils.audio.play_music(file)

    def unmount(self):
         utils.audio.fadeout_music()
         
    def update_skybox(self):
        i = 0

        for skybox in self.skybox_positions:
            self.screen.blit(self.skybox_image, skybox)

            x, y = skybox

            if x < self.skybox_image.get_width() * -1.0:
                x = float(self.skybox_image.get_width())

            x -= 0.1

            self.skybox_positions[i] = (x, y)
            i += 1