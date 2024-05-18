""" Main menu """

import logging
import os

import arcade.gui

import utils.gui
import utils.text
from constants.difficulty import Difficulty
from constants.fonts import FONT_ADRIP
from constants.maps import FIRST_MAP
from state.savegamestate import SaveGameState
from utils.audio import streaming_enabled
from views.difficultyselection import DifficultySelection
from views.fading import Fading
from views.settings.settingsmenu import SettingsMenu

BUTTON_WIDTH = 250
BUTTON_MARGIN_BOTTOM = 20

COLOR_BACKGROUND = (123, 84, 148)


class MainMenu(Fading):
    """ Main menu """

    def __init__(self, window, state):
        """
        Constructor
        @param window: arcade.Window
        @param state: SettingsState
        """
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)
        self.background = COLOR_BACKGROUND

        label = arcade.gui.UILabel(
            text=_('Grunzi'),
            font_name=FONT_ADRIP,
            font_size=utils.text.LOGO_FONT_SIZE,
            text_color=arcade.csscolor.HOTPINK,
            align='center',
        )

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

        options_button = arcade.gui.UIFlatButton(
            text=_("Settings"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        quit_button = arcade.gui.UIFlatButton(
            text=_("Quit game"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        self.player = None

        size = self.window.size
        self.shadertoy = self.state.load_shader(size, 'pigs')

        @newgame_button.event("on_click")
        def on_click_newgame_button(event):
            self.on_new_game()

        @continue_button.event("on_click")
        def on_click_continue_button(event):
            # Pass already created view because we are resuming.

            from views.game import Game
            savegame = SaveGameState.load()

            if not savegame.current:
                savegame.current = FIRST_MAP
            self.state.map_name = savegame.current
            self.state.difficulty = Difficulty(savegame.difficulty, self.state.map_name, self.state.map_dir)

            self.next_view = Game(self.window, self.state)
            self.fade_out()

        @select_map_button.event("on_click")
        def on_click_select_map_button(event):
            # Pass already created view because we are resuming.

            from views.mapselection import MapSelection
            savegame = SaveGameState.load()
            self.state.map_name = savegame.current
            self.state.difficulty = Difficulty(savegame.difficulty, self.state.map_name, self.state.map_dir)

            self.next_view = MapSelection(self.window, self.state, previous_view=self)
            self.fade_out()

        @highscore_button.event("on_click")
        def on_highscore_button(event):

            # Pass already created view because we are resuming.
            from views.highscore import Highscore

            self.next_view = Highscore(self.window, self.state, previous_view=self)
            self.fade_out()

        @options_button.event("on_click")
        def on_click_options_button(event):
            # Pass already created view because we are resuming.

            self.window.show_view(
                SettingsMenu(self.window, self.state, previous_view=self, shadertoy=self.shadertoy, time=self.time)
            )

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.fade_quit()

        widgets = [
            label,
            newgame_button
        ]

        if SaveGameState.exists():
            widgets += [continue_button, select_map_button]

        widgets += [
            highscore_button,
            options_button,
            quit_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()
        self.state.settings.unmute()
        self.window.set_mouse_visible(True)
        self.push_controller_handlers()

        music = None

        try:
            music = arcade.load_sound(
                os.path.join(self.state.music_dir, 'menu.ogg'),
                streaming=streaming_enabled()
            )
        except FileNotFoundError as e:
            logging.error(e)

        if not self.player and music:
            self.player = music.play(loop=True, volume=self.state.settings.music_volume)
        self.manager.enable()

    def on_hide_view(self) -> None:
        """ On hide view """

        super().on_hide_view()
        self.pop_controller_handlers()
        self.manager.disable()

        if self.next_view:
            if self.player:
                self.player.pause()

    def on_new_game(self) -> None:
        """ On click "New Game" show difficulty selection """
        self.next_view = DifficultySelection(
            self.window,
            self.state,
            previous_view=self
        )

        self.fade_out()

    def on_update(self, delta_time: float) -> None:
        """ on update """

        super().on_update(delta_time=delta_time)

        self.update_mouse()
        self.update_fade(self.next_view)

        if self.player and self.player.volume != self.state.settings.music_volume:
            self.player.volume = self.state.settings.music_volume

    def on_draw(self) -> None:
        """ on draw """

        # self.clear()
        # Clear the screen
        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()
        self.draw_build_version()
        self.draw_fading()
        self.draw_debug()
