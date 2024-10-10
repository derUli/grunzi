""" Difficulty selection """

import constants.controls.controller as controller
import constants.controls.keyboard as keyboard
from state.savegamestate import SaveGameState
from utils.text import create_text, FONT_SIZE_LARGE, MARGIN, FONT_SIZE_HEADLINE
from views.fading import Fading

MARGIN_SCORE = 50

COLOR_BACKGROUND = (217, 102, 157)

FILL_COUNT = 6
FILL_CHAR = '0'


class LevelCompleted(Fading):
    """ Difficulty selection """

    def __init__(self, window, state, next_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.next_view = next_view
        self.shadertoy = self.state.load_shader(window.size, 'pink')
        self.background = COLOR_BACKGROUND
        self.texts = []
        self._call_method = None

        self.savegame = SaveGameState.load()

    def on_show_view(self) -> None:
        """ This is run once when we switch to this view """

        super().on_show_view()
        self.setup()

    def on_hide_view(self) -> None:
        """ This is run before this view is hidden """

        super().on_hide_view()
        self.pop_controller_handlers()

    def setup(self) -> None:
        """ Setup the view """

        self._call_method = None
        self.push_controller_handlers()

        self.window.set_mouse_visible(False)

        self.texts = []

        press_button_text = create_text(
            text=_('Press any key to continue'),
            font_size=FONT_SIZE_LARGE
        )

        press_button_text.x = self.window.width / 2 - press_button_text.content_width / 2
        press_button_text.y = MARGIN

        self.texts.append(press_button_text)

        level_completed = create_text(
            text=_('Map completed').upper(),
            font_size=FONT_SIZE_HEADLINE,
            bold=True
        )

        level_completed.x = (self.window.width / 2 - level_completed.content_width / 2)
        level_completed.y = self.window.height / 2 - level_completed.content_height / 2

        self.texts.append(level_completed)

    def on_key_press(self, key, modifiers) -> None:
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if key in keyboard.KEY_DISCARD:
            self.on_continue()

    def on_button_press(self, joystick, key) -> None:
        """ On button press """

        if key in controller.KEY_DISCARD:
            self._call_method = self.on_continue

    def on_update(self, delta_time: float) -> None:
        """ Update the screen """
        super().on_update(delta_time)

        if self._call_method:
            self._call_method()
            self._call_method = None

        self.update_fade(self.next_view)

    def on_draw(self) -> None:
        """ On draw """
        self.camera_gui.use()
        self.render_shadertoy()

        for text in self.texts:
            text.draw()

        self.draw_fading()
        self.draw_after(draw_version_number=True)

    def on_continue(self) -> None:
        """ On click "Back" button """

        self.fade_to_view(self.next_view)
