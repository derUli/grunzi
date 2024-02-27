import arcade.gui

import constants.controls.keyboard
import utils
from utils.text import get_style
from views.fading import Fading
from views.mainmenu import MainMenu
from views.optionsmenu import OptionsMenu

BUTTON_WIDTH = 250
BUTTON_MARGIN_BOTTOM = 20


class PauseMenu(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view=None):
        super().__init__(window)

        self.window = window
        self.manager = arcade.gui.UIManager(window)

        self.state = state

        v_box = arcade.gui.UIBoxLayout()

        continue_button = arcade.gui.UIFlatButton(
            text=_("Continue"),
            width=BUTTON_WIDTH,
            style=get_style()
        )

        options_help = arcade.gui.UIFlatButton(
            text=_("Options & Help"),
            width=BUTTON_WIDTH,
            stye=utils.text.get_style()
        )

        quit_button = arcade.gui.UIFlatButton(
            text=_("Back to main menu"),
            width=BUTTON_WIDTH,
            style=get_style()
        )

        self.previous_view = previous_view

        size = self.window.size()
        self.shadertoy = self.state.load_shader(size, 'gloopy')

        self.time = 0

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

        buttons = [
            continue_button,
            options_help,
            quit_button
        ]

        for button in buttons:
            v_box.add(button.with_space_around(bottom=BUTTON_MARGIN_BOTTOM))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box)
        )

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_toggle()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_toggle(self):
        self.window.show_view(self.previous_view)

    def on_exit(self):
        self.next_view = MainMenu(self.window, self.state)
        self.fade_out()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.manager.enable()

    def on_update(self, dt):
        self.update_fade(self.next_view)
        self.scene.update()

        self.time += dt

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()

        arcade.start_render()
        self.shadertoy.render(time=self.time)

        self.manager.draw()

        self.draw_build_version()

        if self.next_view:
            self.draw_fading()

        self.draw_debug()