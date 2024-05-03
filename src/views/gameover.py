import logging

import constants.controls.keyboard
from constants.controls.joystick import JOYSTICK_BUTTON_MAPPING
from views.fading import Fading
from views.mainmenu import MainMenu


class GameOver(Fading):
    """Main menu view class."""

    def __init__(self, window, state):
        super().__init__(window)

        self.window = window
        self.state = state
        self.shadertoy = self.state.load_shader(window.size, 'gameover')
        self.time = 0

        self.difficulty = None
        self.maps = []
        self.select_button = None
        self.selected = 0

        self._call_method = None

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()

        self.push_controller_handlers()

        self.window.set_mouse_visible(False)

    def on_hide_view(self) -> None:
        """ On hide view """
        self.window.set_mouse_visible(True)
        self.pop_controller_handlers()

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_DISCARD:
            self.on_main_menu()

    def on_button_press(self, controller, key):
        logging.info(f"Controller button {key} pressed")

        if key in constants.controls.controller.KEY_DISCARD:
            self._call_method = self.on_main_menu

    def on_joybutton_press(self, controller, key):
        if str(key) in JOYSTICK_BUTTON_MAPPING:
            button = JOYSTICK_BUTTON_MAPPING[str(key)]
            self.on_button_press(controller, button)

    def on_update(self, delta_time) -> None:
        """ On update """

        # There is an OpenGL error happens when a sprite is added by an controller event handler
        # which seems to happen because the controller events are handled in a different thread.
        # To work around this we have the _call_method class variable which can be set to a class method
        # Which is called in next execution of on_update
        if self._call_method:
            self._call_method()
            self._call_method = None

        super().on_update(delta_time)

        self.time += delta_time

        self.update_mouse()
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()
        self.render_shadertoy()

        self.draw_build_version()

        self.draw_fading()
        self.draw_debug()

    def on_main_menu(self) -> None:
        """ On main menu """
        self.next_view = MainMenu(self.window, self.state)
        self.fade_out()
