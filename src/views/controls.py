import arcade.gui

import constants.controls.keyboard
import utils.text
from views.fading import Fading

BUTTON_WIDTH = 250

MARGIN = 50

URL_GRUNZBABE_AT_X = "https://x.com/GrunzBabe"


LOREM_IPSUM = (
    "↑→↓←Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eget pellentesque velit. "
    "Nam eu rhoncus nulla. Fusce ornare libero eget ex vulputate, vitae mattis orci eleifend. "
    "Donec quis volutpat arcu. Proin lacinia velit id imperdiet ultrices. Fusce porta magna leo, "
    "non maximus justo facilisis vel. Duis pretium sem ut eros scelerisque, a dignissim ante "
    "pellentesque. Cras rutrum aliquam fermentum. Donec id mollis min."
)


class Controls(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)

        self.previous_view = previous_view

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_back(self):
        self.next_view = self.previous_view
        self.fade_out()

    def on_show_view(self):
        super().on_show_view()
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])


        v_box = arcade.gui.UIBoxLayout()

        text_area = arcade.gui.UITextArea(
            width=640,
            height=480,
            text=LOREM_IPSUM * 5,
            font_size=18,
            text_color=(0, 0, 0, 255),
            multiline=True,
        )

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            stye=utils.text.get_style()
        )

        @back_button.event("on_click")
        def on_click_back_button(event):
            # Pass already created view because we are resuming.

            self.on_back()

        buttons = [
            text_area,
            back_button
        ]

        for button in buttons:
            v_box.add(button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box
            )
        )

        self.time = 0

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

        self.manager.draw()

        self.draw_fading()
