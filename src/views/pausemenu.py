import os

import arcade.gui

import constants.controls.keyboard
import utils
from sprites.backdrops.scrollingbackdrop import ScrollingBackdrop
from utils.text import get_style
from views.fading import Fading
from views.mainmenu import MainMenu

BUTTON_WIDTH = 250


class PauseMenu(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view=None):
        super().__init__(window)

        self.window = window
        self.manager = arcade.gui.UIManager(window)

        self.state = state

        v_box = arcade.gui.UIBoxLayout()

        continue_button = arcade.gui.UIFlatButton(text=_("Continue"), width=BUTTON_WIDTH, style=get_style())
        quit_button = arcade.gui.UIFlatButton(text=_("Back to main menu"), width=BUTTON_WIDTH, style=get_style())

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

        self.previous_view = previous_view

        @continue_button.event("on_click")
        def on_click_continue_button(event):
            # Pass already created view because we are resuming.
            self.on_toggle()

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.on_exit()

        buttons = [
            continue_button,
            quit_button
        ]

        for button in buttons:
            v_box.add(button.with_space_around(bottom=20))

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

        self.camera_gui.move_to(
            (
                self.backdrop.center_x - (self.camera_gui.viewport_width / 2),
                self.backdrop.center_y - (self.camera_gui.viewport_height / 2)
            )
        )

        self.manager.enable()

    def on_update(self, dt):
        self.update_fade(self.next_view)
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

        if self.next_view:
            self.draw_fading()
