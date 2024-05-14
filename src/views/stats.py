""" Difficulty selection """

import logging

import constants.controls.controller as controller
import constants.controls.keyboard as keyboard
from constants.controls.joystick import joystick_button_to_controller
from utils.text import create_text, LARGE_FONT_SIZE, MARGIN
from views.fading import Fading

COLOR_BACKGROUND = (217, 102, 157)


class Stats(Fading):
    """ Difficulty selection """

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.previous_view = previous_view
        self.shadertoy = self.state.load_shader(window.size, 'hills')
        self.background = COLOR_BACKGROUND
        self.texts = []

    def on_show_view(self) -> None:
        """ This is run once when we switch to this view """
        super().on_show_view()
        self.push_controller_handlers()
        self.setup()

    def on_hide_view(self) -> None:
        """ This is run before this view is hidden """

        super().on_hide_view()
        self.pop_controller_handlers()

        if self.previous_view.player:
            self.previous_view.player.pause()

    def setup(self) -> None:
        """ Setup the view """

        self.texts = []

        press_button_text = create_text(
            text=_('Press any key to continue'),
            font_size=LARGE_FONT_SIZE
        )

        press_button_text.x = self.window.width / 2 - press_button_text.content_width / 2
        press_button_text.y = MARGIN

        self.texts.append(press_button_text)

        self.window.set_mouse_visible(False)

    def on_key_press(self, key, modifiers) -> None:
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if key in keyboard.KEY_DISCARD:
            self.on_back()

    def on_button_press(self, joystick, key):
        logging.info(f"Controller button {key} pressed")

        if key in controller.KEY_DISCARD:
            self.on_back()

    def on_joybutton_press(self, controller, key):
        self.on_button_press(
            controller,
            joystick_button_to_controller(key)
        )

    def on_update(self, delta_time) -> None:
        """ Update the screen """
        super().on_update(delta_time)

        self.update_fade(self.next_view)

    def on_draw(self) -> None:
        """ On draw """

        self.clear()
        self.camera_gui.use()
        self.render_shadertoy()
        self.draw_build_version()

        for text in self.texts:
            text.draw()

        self.draw_fading()
        self.draw_debug()

    def on_back(self) -> None:
        """ On click "Back" button """
        from views.mainmenu import MainMenu
        self.next_view = MainMenu(self.window, self.state)
        self.fade_out()
