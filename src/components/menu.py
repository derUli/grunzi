import pygame_menu
import constants.game
import components.maingame
from components.settings import Settings
from components.component import Component
import utils.savegame
import gettext
from utils.animation import Animation
from utils.menu import make_menu
import os
import pygame

_ = gettext.gettext


class Menu(Component):

    def __init__(self, data_dir, handle_change_component):
        """ Constructor """
        super().__init__(data_dir, handle_change_component)

        video_path = os.path.join(
            data_dir,
            'images',
            'sprites',
            'animations',
            'dancing_pig')
        # 25 Frames by second
        self.video = Animation(
            video_path,
            refresh_interval=1 / 25,
            size=constants.game.SCREEN_SIZE,
            async_load=True
        )
        self.menu = None

    def mount(self):
        if not pygame.mixer.music.get_busy():
            self.play_music('menu.ogg')

    def update_screen(self, screen):
        self.draw_menu(self.screen)

    def handle_new_game(self):
        self.handle_change_component(components.maingame.MainGame)
        self.menu.disable()

    def handle_continue_game(self):
        component = self.handle_change_component(components.maingame.MainGame)
        component.load_savegame()
        if self.menu:
            self.menu.disable()

    def handle_settings(self):
        component = self.handle_change_component(Settings)
        component.video = self.video
        self.menu.disable()

    def draw_background(self):
        self.screen.blit(self.video.get_frame(), (0, 0))

    def draw_menu(self, screen):
        menu = make_menu(_('Grunzi'), screen)
        menu.add.button(_('New Game'), self.handle_new_game)
        if utils.savegame.has_savegame(utils.savegame.DEFAULT_SAVE):
            menu.add.button(
                _('Continue'),
                self.handle_continue_game)  # Continue game

        menu.add.button(_('Settings'), self.handle_settings)

        menu.add.button(_('Quit'), pygame_menu.events.EXIT)

        self.menu = menu
        menu.mainloop(screen, self.draw_background)
