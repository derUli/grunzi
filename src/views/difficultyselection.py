""" Difficulty selection """

import logging

import arcade.gui

import constants.controls.keyboard
import utils.gui
import utils.text
from constants.difficulty import DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD, Difficulty
from constants.fonts import FONT_DEFAULT
from state.savegamestate import SaveGameState, new_savegame
from views.fading import Fading

BUTTON_WIDTH = 250


class DifficultySelection(Fading):
    """ Difficulty selection """

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.previous_view = previous_view
        self.manager = arcade.gui.UIManager(window)
        self.shadertoy = self.state.load_shader(window.size, 'pink')
        self.time = 0

        self.difficulty = None

    def on_show_view(self) -> None:
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        self.setup()

    def on_hide_view(self) -> None:
        """ This is run before this view is hidden """
        self.pop_controller_handlers()
        self.manager.disable()

        if self.previous_view.player:
            self.previous_view.player.pause()

    def setup(self) -> None:
        """ Setup the view """
        self.manager.clear()
        self.manager.disable()

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        difficulty_easy = arcade.gui.UIFlatButton(
            text=_("Easy"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        difficulty_medium = arcade.gui.UIFlatButton(
            text=_("Medium"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        difficulty_high = arcade.gui.UIFlatButton(
            text=_("High"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        @difficulty_easy.event("on_click")
        def on_click_easy(event):
            # Pass already created view because we are resuming.
            self.on_select_difficulty(DIFFICULTY_EASY)

        @difficulty_medium.event("on_click")
        def on_click_medium(event):
            # Pass already created view because we are resuming.
            self.on_select_difficulty(DIFFICULTY_MEDIUM)

        @difficulty_high.event("on_click")
        def on_click_hard(event):
            # Pass already created view because we are resuming.
            self.on_select_difficulty(DIFFICULTY_HARD)

        @back_button.event("on_click")
        def on_click_back_button(event):
            # Pass already created view because we are resuming.

            self.on_back()

        title = arcade.gui.UILabel(
            text=_('Difficulty'),
            font_name=FONT_DEFAULT,
            font_size=utils.text.HEADLINE_FONT_SIZE,
            text_color=arcade.csscolor.HOTPINK,
            align='center'
        )

        widgets = [
            title,
            back_button,
            difficulty_easy,
            difficulty_medium,
            difficulty_high
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

        if self.previous_view.player:
            self.previous_view.player.play()

    def on_key_press(self, key, modifiers) -> None:
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, delta_time) -> None:
        """ Update the screen """
        super().on_update(delta_time)

        self.time += delta_time

        self.update_mouse()
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self) -> None:
        """ On draw """

        # Clear the screen
        self.clear()
        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()
        self.draw_build_version()

        self.draw_fading()
        self.draw_debug()

    def on_select_difficulty(self, difficulty, overwrite=False) -> None:
        """ On select difficulty """

        self.difficulty = difficulty

        if SaveGameState.exists() and not overwrite:
            return self.on_confirm_overwrite_savegame()

        logging.info(utils.text.label_value('Difficulty', difficulty))

        if self.previous_view.player:
            self.previous_view.player.pause()

        new_savegame(self.state.map_name_first, difficulty)

        self.state.map_name = self.state.map_name_first
        self.state.difficulty = Difficulty(difficulty, self.state.map_name, self.state.map_dir)

        from views.game import Game

        self.next_view = Game(self.window, self.state)
        self.fade_out()

    def on_back(self) -> None:
        """ On click "Back" button """
        from views.mainmenu import MainMenu
        self.next_view = MainMenu(self.window, self.state)
        self.fade_out()

    def on_confirm_overwrite_savegame(self) -> None:
        """ Show confirm overwrite savegame dialog """
        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=_('Overwrite existing savegame?'),
            buttons=[
                _("Yes"),
                _("No")
            ]
        )

        message_box.on_action = self.on_overwrite_savegame

        self.manager.add(message_box)

    def on_overwrite_savegame(self, event) -> None:
        """ On overwrite savegame """
        action = event.action
        if action == _('Yes'):
            self.on_select_difficulty(self.difficulty, overwrite=True)
