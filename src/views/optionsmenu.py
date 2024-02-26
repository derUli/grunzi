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

        v_box = arcade.gui.UIBoxLayout()

        controls_button = arcade.gui.UIFlatButton(
            text=_("Controls"),
            width=BUTTON_WIDTH,
            stye=utils.text.get_style()
        )

        grunzbabe_at_x_button = arcade.gui.UIFlatButton(
            text=_("Follow me on X"),
            width=BUTTON_WIDTH,
            stye=utils.text.get_style()
        )

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            stye=utils.text.get_style()
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

        buttons = [
            controls_button,
            grunzbabe_at_x_button,
            back_button
        ]

        for button in buttons:
            v_box.add(button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box)
        )

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_back(self):
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)

    def on_show_view(self):
        super().on_show_view()
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])
        self.manager.enable()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, dt):
        self.scene.update()
        self.time += dt
        self.update_fade(self.next_view)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()

        arcade.start_render()
        self.shadertoy.render(time=self.time)

        self.manager.draw()

        self.draw_build_version()

        self.draw_fading()
