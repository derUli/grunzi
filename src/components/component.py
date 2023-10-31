import pygame
import os
import constants.game
import constants.headup

class Component(object):
    def __init__(self, data_dir, handle_change_component):
        self.monotype_font = pygame.font.Font(
            os.path.join(
                data_dir,
                'fonts',
                constants.game.MONOTYPE_FONT),
            constants.game.DEBUG_OUTPUT_FONT_SIZE
            )

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