import os
import webbrowser

import arcade.gui
import constants.controls.keyboard
import utils.text
from sprites.backdrops.scrollingbackdrop import ScrollingBackdrop
from views.view import View

BUTTON_WIDTH = 250

URL_GRUNZBABE_AT_X = "https://x.com/GrunzBabe"


class OptionsMenu(View):
    """Main menu view class."""

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)

        self.previous_view = previous_view

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

        self.backdrop = ScrollingBackdrop(
            filename=os.path.join(
                self.state.image_dir,
                'backdrops',
                'menu.jpg'
            ),
        )
        self.backdrop.width = self.window.width
        self.backdrop.height = self.window.height

        self.scene.add_sprite('backdrop', self.backdrop)

        # A non-scrolling camera that can be used to draw GUI elements

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
            #controls_button,
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
        self.window.show_view(self.previous_view)

    def on_show_view(self):
        super().on_show_view()
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        self.camera_gui.move_to(
            (
                self.backdrop.center_x - (self.camera_gui.viewport_width / 2),
                self.backdrop.center_y - (self.camera_gui.viewport_height / 2)
            )
        )

        self.manager.enable()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()
    def on_update(self, dt):
        self.scene.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()

        self.camera_gui.use()

        self.scene.draw()
        self.manager.draw()

        build_version = os.path.join(self.state.root_dir, 'VERSION.txt')
        utils.text.draw_build_number(build_version, self.window)
