import gettext

from components.component import Component

_ = gettext.gettext

FADE_IN = 1
FADE_OUT = 2

FADE_SPEED = 5


class FadeableComponent(Component):
    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad):
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)
        self.alpha = 0
        self.do_fade = None

    def fadein(self):
        self.do_fade = FADE_IN

    def fadeout(self):
        self.do_fade = FADE_OUT

    def fade(self):
        if self.do_fade == FADE_IN:
            self.alpha += FADE_SPEED
            if self.alpha >= 255:
                self.do_fade = None
        elif self.do_fade == FADE_OUT:
            self.alpha -= -1
            if self.alpha <= 0:
                self.do_fade = None
