""" Controls Screen """
import os
import random
import time

from components.menu.mainmenu import MainMenu
from components.menu.menucomponent import MenuComponent
from components.mixins.filmgrain import FilmGrain
from constants.headup import PIGGY_PINK
from utils.audio import play_sound

PAGE_KEYBOARD = 0
PAGE_CONTROLLER = 1

BACKGROUND = PIGGY_PINK

PHASE_FADEIN = 1
PHASE_WAIT = 2
PHASE_FADEOUT = 3
FADE_SPEED = 1
WAIT = 3

class Intro(MenuComponent):
    """ Controls screen """

    def __init__(self, data_dir, handle_change_component,
                 settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(
            data_dir,
            handle_change_component,
            settings_state,
            enable_edit_mode,
            gamepad)
        self.menu = None
        self.backdrop = None
        self.alpha = 0
        self.phase = PHASE_FADEIN
        self.wait_for = None


    def draw(self, screen):
        """ Update screen """
        if not self.backdrop:
            file = os.path.join(
                self.data_dir,
                'images',
                'ui',
                'logo.png'
            )

            self.backdrop = self.image_cache.load_image(file)

        x = screen.get_width() / 2 - self.backdrop.get_width() / 2
        y = screen.get_height() / 2 - self.backdrop.get_height() / 2

        self.backdrop.set_alpha(self.alpha)
        screen.fill(BACKGROUND)

        screen.blit(self.backdrop, (x, y))
        self.fade()

    def fade(self):

        if self.phase == PHASE_FADEIN:
            self.alpha += FADE_SPEED

            if self.alpha > 255:
                self.alpha = 255
                self.phase = PHASE_WAIT
                self.wait_for = time.time() + WAIT

                play_sound(
                    os.path.join(
                        self.data_dir,
                        'sounds',
                        'pig',
                        'grunt' + str(random.randint(1, 5)) + '.ogg'
                    )
                )

        elif self.phase == PHASE_WAIT:
            if time.time() > self.wait_for:
                self.phase = PHASE_FADEOUT

        elif self.phase == PHASE_FADEOUT:
            self.alpha -= FADE_SPEED

            if self.alpha < 0:
                self.alpha = 0

                self.handle_change_component(MainMenu)