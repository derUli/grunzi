import os
import arcade.gui

import utils
from sprites.backdrops.scrollingbackdrop import ScrollingBackdrop

from views.mainmenuview import MainMenuView
from views.view import View


class PauseMenuView(View):
    """Main menu view class."""

    def __init__(self, window, state, previous_view = None):
        super().__init__(window)

        self.window = window
        self.manager = arcade.gui.UIManager(window)

        self.state = state

        v_box = arcade.gui.UIBoxLayout()

        newgame_button = arcade.gui.UIFlatButton(text=_("Continue"), width=200)

        quit_button = arcade.gui.UIFlatButton(text=_("Back to main menu"), width=200)

        self.scene = arcade.Scene()

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

        self.next_view = None
        # A non-scrolling camera that can be used to draw GUI elements
        self.camera_gui = None

        self.previous_view = previous_view

        @newgame_button.event("on_click")
        def on_click_newgame_button(event):
            # Pass already created view because we are resuming.
            self.window.show_view(self.previous_view)

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.window.show_view(MainMenuView(self.window, self.state))

        buttons = [
            newgame_button,
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

        self.state = state

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        self.camera_gui = arcade.Camera()

        self.camera_gui.move_to(
            (
                self.backdrop.center_x - (self.camera_gui.viewport_width / 2),
                self.backdrop.center_y - (self.camera_gui.viewport_height / 2)
            )
        )

        self.manager.enable()

    def on_update(self, dt):
        self.scene.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()

        self.scene.draw()
        self.manager.draw()

        build_version = os.path.join(self.state.root_dir, 'VERSION')
        utils.text.draw_build_number(build_version, self.window)