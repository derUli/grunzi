""" Difficulty selection """

import constants.controls.controller as controller
import constants.controls.keyboard as keyboard
from constants.fonts import FONT_MONOTYPE
from state.savegamestate import SaveGameState
from utils.highscore import HighscoreStorage
from utils.text import create_text, FONT_SIZE_LARGE, MARGIN, FONT_SIZE_EXTRA_LARGE
from views.fading import Fading

MARGIN_SCORE = 50

COLOR_BACKGROUND = (217, 102, 157)

FILL_COUNT = 6
FILL_CHAR = '0'


class HighscoreList(Fading):
    """ Difficulty selection """

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.previous_view = previous_view
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

        if self.previous_view.player:
            self.previous_view.player.play()

        self.window.set_mouse_visible(False)

        self.texts = []

        press_button_text = create_text(
            text=_('Press any key to continue'),
            font_size=FONT_SIZE_LARGE
        )

        press_button_text.x = self.window.width / 2 - press_button_text.content_width / 2
        press_button_text.y = MARGIN

        self.texts.append(press_button_text)

        labels = []
        scores = []

        storage = HighscoreStorage()
        storage.fetch()

        highscore = storage.highscore

        if self.window.height <= 768:
            highscore = highscore[:5]

        for entry in highscore:
            labels.append(str(entry['name']))
            scores.append(str(entry['score']).rjust(FILL_COUNT, FILL_CHAR))

        if len(labels) == 0:
            labels.append(_('No entries yet'))

        score_text_left = create_text(
            text="\n\n".join(labels),
            font_size=FONT_SIZE_EXTRA_LARGE,
            font_name=FONT_MONOTYPE,
            width=self.window.width / 2,
            multiline=True,
            bold=True
        )

        score_text_right = create_text(
            text="\n\n".join(scores),
            font_size=FONT_SIZE_EXTRA_LARGE,
            font_name=FONT_MONOTYPE,
            width=self.window.width / 2,
            multiline=True,
            bold=True
        )

        score_text_left.x = MARGIN
        score_text_left.y = self.window.height - score_text_left.content_height - MARGIN_SCORE
        self.texts.append(score_text_left)

        score_text_right.x = self.window.width - MARGIN - score_text_right.content_width
        score_text_right.y = score_text_left.y
        self.texts.append(score_text_right)

    def on_key_press(self, key, modifiers) -> None:
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if key in keyboard.KEY_DISCARD:
            self.on_back()

    def on_button_press(self, joystick, key) -> None:
        """ On button press """

        if key in controller.KEY_DISCARD:
            self._call_method = self.on_back

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

    def on_back(self) -> None:
        """ On click "Back" button """

        from views.menu.mainmenu import CampaignMenu
        self.fade_to_view(CampaignMenu(self.window, self.state, previous_view=self.previous_view))
