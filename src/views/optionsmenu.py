import webbrowser

import arcade.gui

import constants.controls.keyboard
import utils.text
from views.controls import Controls
from views.fading import Fading

BUTTON_WIDTH = 250
URL_GRUNZBABE_AT_X = "https://x.com/GrunzBabe"


class OptionsMenu(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view, shadertoy, time=0):
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)
        self.shadertoy = shadertoy
        self.time = time

        self.previous_view = previous_view
        self._fade_in = None

        controls_button = arcade.gui.UIFlatButton(
            text=_("Controls"),
            width=BUTTON_WIDTH,
            style=utils.text.get_style()
        )

        grunzbabe_at_x_button = arcade.gui.UIFlatButton(
            text=_("Follow me on X"),
            width=BUTTON_WIDTH,
            style=utils.text.get_style()
        )

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.text.get_style()
        )

        @controls_button.event("on_click")
        def on_click_controls_button(event):
            comeback_view = OptionsMenu(self.window, self.state, self.previous_view, self.shadertoy, 0)

            # Pass already created view because we are resuming.
            self.next_view = Controls(self.window, self.state, comeback_view)
            self.fade_out()

        @grunzbabe_at_x_button.event("on_click")
        def on_click_grunzbabe_at_x_button(event):
            # Pass already created view because we are resuming.
            self.window.set_fullscreen(self.window.fullscreen)
            webbrowser.open(URL_GRUNZBABE_AT_X)

        @back_button.event("on_click")
        def on_click_back_button(event):
            # Pass already created view because we are resuming.

            self.on_back()

        widgets = [
            controls_button,
            grunzbabe_at_x_button,
            back_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.pop_controller_handlers()
        self.manager.disable()

    def on_back(self):
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])
        self.manager.enable()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, dt):
        self.time += dt

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

        self.draw_fading()
        self.draw_debug()
