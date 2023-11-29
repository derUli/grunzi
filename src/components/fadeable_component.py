import pygame

from components.component import Component

FADE_IN = 1
FADE_OUT = 2

FADE_SPEED = 2.55


class FadeableComponent(Component):

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.alpha = 0
        self.do_fade = None
        self.fade_speed = FADE_SPEED

    def fadein(self):
        """ Start fade in """
        self.do_fade = FADE_IN
        self.alpha = 0

    def fadeout(self):
        """ Start fade out """
        self.do_fade = FADE_OUT
        self.alpha = 255

    def fade(self):
        """ Do fade step """
        if self.do_fade == FADE_IN:
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.do_fade = None
        elif self.do_fade == FADE_OUT:
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                self.do_fade = None
                self.alpha = 0

    def mount(self):
        """ Fadein on Mount """
        self.fadein()

    def unmount(self):
        """ Fadeout music on unmount """
        pygame.mixer.music.fadeout(1000)
