import arcade.gui

import constants.controls.keyboard
import utils
from utils.text import get_style
from views.fading import Fading
from views.mainmenu import MainMenu
from views.optionsmenu import OptionsMenu

BUTTON_WIDTH = 250


class PauseMenu(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view=None):
        super().__init__(window)

        self.window = window
        self.manager = arcade.gui.UIManager(window)

        self.state = state

        continue_button = arcade.gui.UIFlatButton(
            text=_("Continue"),
            width=BUTTON_WIDTH,
            style=get_style()
        )

        options_help = arcade.gui.UIFlatButton(
            text=_("Options & Help"),
            width=BUTTON_WIDTH,
            style=utils.text.get_style()
        )

        quit_button = arcade.gui.UIFlatButton(
            text=_("Back to main menu"),
            width=BUTTON_WIDTH,
            style=get_style()
        )

        self.previous_view = previous_view

        size = self.window.size
        self.shadertoy = self.state.load_shader(size, 'gloopy')

        @continue_button.event("on_click")
        def on_click_continue_button(event):
            # Pass already created view because we are resuming.
            self.on_toggle()

        @options_help.event("on_click")
        def on_click_options_help(event):
            # Pass already created view because we are resuming.

            self.window.show_view(
                OptionsMenu(
                    self.window,
                    self.state,
                    previous_view=self,
                    shadertoy=self.shadertoy,
                    time=self.time
                ),
            )

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.on_exit()

        widgets = [
            continue_button,
            options_help,
            quit_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_toggle()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()
        self.push_controller_handlers()
        self.manager.enable()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.pop_controller_handlers()
        self.manager.disable()

    def on_toggle(self):
        self.window.show_view(self.previous_view)

    def on_exit(self):
        self.next_view = MainMenu(self.window, self.state)
        self.fade_out()

    def on_update(self, delta_time):
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

        self.manager.draw()
        self.draw_build_version()

        if self.next_view:
            self.draw_fading()

        self.draw_debug()
