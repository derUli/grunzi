""" Difficulty selection """
import logging

import arcade
import arcade.gui

import constants.controls.keyboard
import constants.fonts
import utils.gui
import utils.text
from state.savegamestate import SaveGameState
from utils.highscore import HighscoreStorage
from views.fading import Fading
from views.highscore.highscorelist import HighscoreList
from views.menu.mainmenu import MainMenu

BUTTON_WIDTH = 250
MARGIN_SCORE = 50

COLOR_BACKGROUND = (71, 181, 230)

FILL_COUNT = 6
FILL_CHAR = '0'
FILL_CHAR_NAME = ' '


class HighscoreAdd(Fading):
    """ Difficulty selection """

    def __init__(self, window, state):
        """ Constructor """
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = None
        self.input_name = None
        self.message_box = None
        self.submitting = False

    def on_show_view(self) -> None:
        """ This is run once when we switch to this view """

        super().on_show_view()

        self.background = COLOR_BACKGROUND
        self.push_controller_handlers()
        self.setup()

    def on_hide_view(self) -> None:
        """ This is run before this view is hidden """

        super().on_hide_view()
        self.pop_controller_handlers()
        self.manager.disable()

    def setup(self) -> None:
        """ Setup the view """

        self.shadertoy = self.state.load_shader(self.window.size, 'waves')
        self.manager = arcade.gui.UIManager(self.window)

        widgets = []

        savegame = SaveGameState.load()

        total_string = _('Total')
        fill_name_len = len(total_string)

        for map in savegame.score:
            formatted_score = str(savegame.score[map]).rjust(FILL_COUNT, FILL_CHAR)
            map_name = map.rjust(fill_name_len, FILL_CHAR_NAME)

            widgets += [
                arcade.gui.UILabel(
                    text=_(f"{map_name}: {formatted_score}"),
                    font_name=constants.fonts.FONT_MONOTYPE,
                    font_size=utils.text.FONT_SIZE_LARGE,
                )
            ]

        formatted_score = str(savegame.total_score).rjust(FILL_COUNT, FILL_CHAR)

        widgets += [
            arcade.gui.UILabel(
                text=' ',
                font_name=constants.fonts.FONT_MONOTYPE,
                font_size=utils.text.FONT_SIZE_MEDIUM,
            ),
            arcade.gui.UILabel(
                text=_(f"{total_string}: {formatted_score}"),
                font_name=constants.fonts.FONT_MONOTYPE,
                font_size=utils.text.FONT_SIZE_LARGE,
            ),
            arcade.gui.UILabel(
                text=' ',
                font_name=constants.fonts.FONT_MONOTYPE,
                font_size=utils.text.FONT_SIZE_LARGE,
            )
        ]

        submit_button = arcade.gui.UIFlatButton(
            text=_("Submit Entry"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style(),
        )

        @submit_button.event('on_click')
        def on_submit(event) -> None:
            logging.debug(event)

            self.on_submit()

        self.input_name = arcade.gui.UIInputText(
            text="",
            width=BUTTON_WIDTH,
            font_name=constants.fonts.FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_INPUT,
        ).with_background(color=arcade.csscolor.WHITE)

        widgets += [
            arcade.gui.UILabel(
                text=_('Please enter your name:'),
                font_name=constants.fonts.FONT_DEFAULT,
                font_size=utils.text.FONT_SIZE_EXTRA_LARGE,
                bold=True
            ),
            self.input_name,
            arcade.gui.UILabel(
                text=_("Leave blank to skip"),
                font_name=constants.fonts.FONT_DEFAULT,
                font_size=utils.text.FONT_SIZE_SMALL,
                bold=True
            ),
            arcade.gui.UILabel(
                text=' ',
                font_name=constants.fonts.FONT_DEFAULT,
                font_size=utils.text.FONT_SIZE_MEDIUM,
            ),
            submit_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

    def show_error(self, event=None) -> None:

        if event:
            self.manager.remove(self.message_box)
            self.message_box = None
            return

        self.message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=_('Submit failed.'),
            buttons=[
                _("OK")
            ]
        )

        self.message_box.show_error = self.show_error

        self.manager.add(self.message_box)

    def show_confirm(self, event=None) -> None:
        if event:
            self.manager.remove(self.message_box)
            self.message_box = None

            if event.action == _('Yes'):
                return self.fade_to_view(MainMenu(self.window, self.state))

            return

        self.message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text="\n".join(
                [
                    _("You have not entered a name."),
                    _("Do you not want to transfer your score?")
                ]
            ),
            buttons=[
                _("Yes"),
                _('No')
            ]
        )

        self.message_box.on_action = self.show_confirm
        self.manager.add(self.message_box)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """ Called whenever a key is pressed. """

        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_CONFIRM:
            self.on_submit()

    def on_submit(self) -> None:
        if self.submitting:
            return

        self.input_name.text = self.input_name.text.strip()

        if len(self.input_name.text) == 0:
            return self.show_confirm()

        self.submitting = True

        if not HighscoreStorage().submit(
                self.input_name.text,
                SaveGameState().load().total_score
        ):
            self.submitting = False
            return self.show_error()

        self.fade_to_view(
            HighscoreList(
                self.window,
                self.state,
                MainMenu(self.window, self.state)
            )
        )

    def on_update(self, delta_time: float) -> None:
        """ Update the screen """

        super().on_update(delta_time)
        self.update_mouse()
        self.update_fade(self.next_view)

    def on_draw(self) -> None:
        """ On draw """

        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()
        self.draw_fading()
        self.draw_after(draw_version_number=True)
