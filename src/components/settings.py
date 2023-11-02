import pygame_menu
import constants.game
from components.component import Component
import utils.savegame
import gettext
from utils.animation import Animation
import os
import pygame

_ = gettext.gettext


class Settings(Component):

    def __init__(self, data_dir, handle_change_component):
        """ Constructor """
        super().__init__(data_dir, handle_change_component)

        video_path = os.path.join(
            data_dir,
            'images',
            'sprites',
            'animations',
            'dancing_pig'
        )
        # 25 Frames by second
        self.video = Animation(
            video_path,
            refresh_interval=1 / 25,
            size=(constants.game.SCREEN_WIDTH, constants.game.SCREEN_HEIGHT),
            async_load=True
        )
        self.menu = None

    def update_screen(self, screen):
        self.draw_menu(self.screen)

    def handle_back(self):
        component = self.handle_change_component(None)
        component.video = self.video
        self.menu.disable()

    def draw_background(self):
        self.screen.blit(self.video.get_frame(), (0, 0))

    def handle_toggle_fullscreen(self):
        pygame.display.toggle_fullscreen()

    def draw_menu(self, screen):
        menu = pygame_menu.Menu(height=300,
                                theme=pygame_menu.themes.THEME_BLUE,
                                title=constants.game.WINDOW_CAPTION,
                                width=screen.get_width() / 3)

        menu.add.button(_('Toggle Fullscreen'), self.handle_toggle_fullscreen)


        menu.add.button(_('Back To Main Menu'), self.handle_back)

        menu.add.button(_('Quit'), pygame_menu.events.EXIT)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
