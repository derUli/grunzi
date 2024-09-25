import logging

import arcade.gui

import constants.controls.keyboard
import utils.gui
import utils.text
from constants.gui import BUTTON_WIDTH
from constants.mapconfig import MapConfig
from constants.maps import FIRST_MAP
from state.savegamestate import SaveGameState
from views.fading import Fading
from views.menu.difficultyselection import DifficultySelection

COLOR_BACKGROUND = (123, 84, 148)


class CampaignMenu(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)

        self.shadertoy = previous_view.shadertoy
        self.player = previous_view.player
        self.time = previous_view.time

        self.previous_view = previous_view
        self._fade_in = None
        self.background = COLOR_BACKGROUND

    def on_show_view(self) -> None:
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        self.setup()

    def on_hide_view(self) -> None:
        super().on_hide_view()
        # Disable the UIManager when the view is hidden.
        self.pop_controller_handlers()
        self.manager.disable()

    def on_back(self) -> None:
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)

    def setup(self) -> None:
        self.manager.clear()
        self.manager.disable()

        newgame_button = arcade.gui.UIFlatButton(
            text=_("New Game"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        continue_button = arcade.gui.UIFlatButton(
            text=_("Continue"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style(),
        )

        select_map_button = arcade.gui.UIFlatButton(
            text=_("Select Map"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style(),
        )

        highscore_button = arcade.gui.UIFlatButton(
            text=_("Online Highscore"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style(),
        )

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        @newgame_button.event("on_click")
        def on_click_newgame_button(event):
            logging.debug(event)
            self.on_new_game()

        @continue_button.event("on_click")
        def on_click_continue_button(event):
            logging.debug(event)
            # Pass already created view because we are resuming.

            from views.game import Game
            savegame = SaveGameState.load()

            if not savegame.current:
                savegame.current = FIRST_MAP
            self.state.map_name = savegame.current
            self.state.difficulty = MapConfig(savegame.difficulty, self.state.map_name, self.state.map_dir)

            self.fade_to_view(Game(self.window, self.state))

        @select_map_button.event("on_click")
        def on_click_select_map_button(event):
            logging.debug(event)

            # Pass already created view because we are resuming.

            from views.menu.mapselection import MapSelection
            savegame = SaveGameState.load()
            self.state.map_name = savegame.current
            self.state.difficulty = MapConfig(savegame.difficulty, self.state.map_name, self.state.map_dir)

            self.fade_to_view(MapSelection(self.window, self.state, previous_view=self.previous_view))

        @highscore_button.event("on_click")
        def on_highscore_button(event):
            logging.debug(event)

            from views.highscore.highscorelist import HighscoreList
            self.fade_to_view(HighscoreList(self.window, self.state, previous_view=self.previous_view))

        @back_button.event("on_click")
        def on_click_back_button(event):
            logging.debug(event)

            # Pass already created view because we are resuming.
            self.on_back()

        widgets = [
            newgame_button,
        ]

        if SaveGameState.exists():
            widgets += [continue_button, select_map_button]

        widgets += [
            highscore_button,
            back_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """ Called whenever a key is pressed """

        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, delta_time: float) -> None:

        super().on_update(delta_time)

        self.update_mouse()
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self) -> None:
        """ Render the screen. """

        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()

        self.draw_fading()
        self.draw_after(draw_version_number=True)

    def on_toggle_fps(self) -> None:
        super().on_toggle_fps()
        self.setup()

    def on_toggle_fullscreen(self) -> None:
        super().on_toggle_fullscreen()
        self.setup()

    def on_new_game(self) -> None:
        """ On click "New Game" show difficulty selection """

        self.fade_to_view(
            DifficultySelection(
                self.window,
                self.state,
                previous_view=self.previous_view,
            )
        )
